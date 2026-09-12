# Verifiable Service Settlement

A GenLayer primitive that releases locked service credits only after validators independently fetch and evaluate public delivery evidence.

## Why GenLayer

Conventional contracts cannot interpret heterogeneous web evidence. Offchain oracles can report a conclusion, but users must trust the reporter. Here, the contract stores source commitments, every validator fetches the same sources, verifies exact content hashes, derives authority domains, checks duplicate content, evaluates delivery criteria, and compares the complete decision-bearing report.

## Lifecycle

`CREDIT → CREATE JOB → PROVIDER ACCEPTS → BIND 2–5 INDEPENDENT SOURCES → FETCH + CONSENSUS → SETTLED / REJECTED / CONFLICTED`

`SETTLED` transfers locked credits to the provider. `REJECTED` and `CONFLICTED` refund the client. All terminal states are immutable.

## Consensus boundary

The leader and validators independently fetch every HTTPS URL and reconstruct exact content hashes, hash-match vector, authority list, duplicate-content flag, evidence-completeness gate, and four semantic delivery decisions. Acceptance requires exact equality of the complete report; there is no confidence tolerance that can cross a threshold.

## Security properties

- No caller supplies the verification outcome or confidence.
- Two or more distinct HTTPS authority domains are mandatory.
- Evidence content must match the precommitted SHA-256 hashes.
- Duplicate content fails closed.
- Only the client triggers settlement; only the named provider can bind evidence.
- Deadlines and terminal states prevent stale replay or repeated settlement.
- The proof root binds parties, terms, amount, deadline, fetched evidence, and decision.

## Commands

```powershell
genvm-lint check contracts/VerifiableServiceSettlement.py
genlayer network set studionet
genlayer deploy --contract contracts/VerifiableServiceSettlement.py
```

See `LIVE_PROOFS.md` for the matching deployed source and finalized lifecycle transactions.
