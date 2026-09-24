import hashlib
import json
import pytest


DEADLINE = 2_000_000_000


def address(value):
    from genlayer import Address
    return Address("0x" + value.hex())


def funded_job(direct_vm, direct_deploy, alice, bob, job_id):
    direct_vm.sender = alice
    direct_vm.warp("2026-09-24T00:00:00Z")
    contract = direct_deploy("contracts/VerifiableServiceSettlement.py")
    contract.grant_demo_credits(address(alice), 100)
    contract.create_job(job_id, address(bob), "public report", "report confirms completion", 30, DEADLINE)
    assert contract.get_balance(address(alice)) == 70
    return contract


def test_client_cancels_unaccepted_job_once(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = funded_job(direct_vm, direct_deploy, direct_alice, direct_bob, "cancel")
    contract.cancel_unaccepted("cancel")
    assert contract.get_job("cancel")["status"] == "CANCELLED"
    assert contract.get_balance(address(direct_alice)) == 100
    with direct_vm.expect_revert("only client may cancel an unaccepted job"):
        contract.cancel_unaccepted("cancel")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("job cannot be accepted"):
        contract.accept_job("cancel")


@pytest.mark.parametrize("stage", ["OPEN", "ACCEPTED", "EVIDENCE_BOUND"])
def test_anyone_refunds_unresolved_after_deadline(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, stage):
    contract = funded_job(direct_vm, direct_deploy, direct_alice, direct_bob, "expire")
    direct_vm.sender = direct_bob
    if stage != "OPEN":
        contract.accept_job("expire")
    if stage == "EVIDENCE_BOUND":
        contract.bind_evidence("expire", "https://a.example/evidence", "0" * 64)
    with direct_vm.expect_revert("job is not expired and unresolved"):
        contract.refund_expired("expire")
    direct_vm.warp("2034-01-01T00:00:00Z")
    from genlayer import gl
    gl.message_raw["datetime"] = "2034-01-01T00:00:00Z"
    direct_vm.sender = direct_charlie
    contract.refund_expired("expire")
    assert contract.get_job("expire")["status"] == "EXPIRED"
    assert contract.get_balance(address(direct_alice)) == 100
    with direct_vm.expect_revert("job is not expired and unresolved"):
        contract.refund_expired("expire")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("provider-only evidence binding"):
        contract.bind_evidence("expire", "https://a.example/evidence", "0" * 64)


def test_provider_settles_without_client_call(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = funded_job(direct_vm, direct_deploy, direct_alice, direct_bob, "settle")
    body_a = "Public report confirms completion."
    body_b = "Independent record confirms report completion."
    direct_vm.sender = direct_bob
    contract.accept_job("settle")
    contract.bind_evidence("settle", "https://a.example/evidence", hashlib.sha256(body_a.encode()).hexdigest())
    contract.bind_evidence("settle", "https://b.example/evidence", hashlib.sha256(body_b.encode()).hexdigest())
    direct_vm.mock_web(r".*a\.example/evidence", {"status": 200, "body": body_a})
    direct_vm.mock_web(r".*b\.example/evidence", {"status": 200, "body": body_b})
    direct_vm.mock_llm(r".*Independently determine.*", json.dumps({
        "deliverable_observed": True,
        "criteria_satisfied": True,
        "sources_consistent": True,
        "no_material_contradiction": True,
    }))
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("party-only verification"):
        contract.verify_and_settle("settle")
    direct_vm.sender = direct_bob
    contract.verify_and_settle("settle")
    assert contract.get_job("settle")["status"] == "SETTLED"
    assert contract.get_balance(address(direct_bob)) == 30
    assert contract.get_balance(address(direct_alice)) == 70
    with direct_vm.expect_revert("party-only verification"):
        contract.verify_and_settle("settle")
