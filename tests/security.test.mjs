import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const source = readFileSync(new URL("../contracts/VerifiableServiceSettlement.py", import.meta.url), "utf8");

test("validators independently fetch committed evidence", () => {
  assert.match(source, /gl\.nondet\.web\.get\(urls\[index\]\)/);
  assert.match(source, /digest == expected_hashes\[index\]/);
  assert.match(source, /not _is_sha256\(expected_sha256\)/);
  assert.match(source, /independent = observe\(\)/);
});

test("decision-bearing report requires exact equality", () => {
  assert.match(source, /"semantic", "observed_hashes", "hash_matches", "authorities"/);
  assert.match(source, /all\(leader\.calldata\.get\(key\) == independent\[key\]/);
  assert.doesNotMatch(source, /confidence/);
});

test("settlement transfers locked credits", () => {
  assert.match(source, /self\.balances\[job\.provider\].*\+ job\.amount/);
  assert.match(source, /job\.status = SETTLED/);
  assert.match(source, /job\.status not in \(ACCEPTED, EVIDENCE_BOUND\)/);
});

test("locked credits have cancellation and deadline recovery paths", () => {
  assert.match(source, /def cancel_unaccepted\(self, job_id: str\)/);
  assert.match(source, /job\.status != OPEN/);
  assert.match(source, /def refund_expired\(self, job_id: str\)/);
  assert.match(source, /job\.status not in \(OPEN, ACCEPTED, EVIDENCE_BOUND\) or _now\(\) < job\.deadline/);
  assert.match(source, /self\._refund\(job_id, job, (CANCELLED|EXPIRED)\)/);
});

test("provider can initiate predeadline evidence settlement", () => {
  assert.match(source, /gl\.message\.sender_address not in \(job\.client, job\.provider\)/);
  assert.match(source, /job\.evidence_count < 2 or _now\(\) >= job\.deadline/);
});
