# Verifiable Service Settlement

A GenLayer primitive that releases locked service credits only after validators independently fetch and evaluate public delivery evidence.

## Why GenLayer

Conventional contracts cannot interpret heterogeneous web evidence. Offchain oracles can report a conclusion, but users must trust the reporter. Here, the contract stores source commitments, every validator fetches the same sources, verifies exact content hashes, derives authority domains, checks duplicate content, evaluates delivery criteria, and compares the complete decision-bearing report.

## Lifecycle

`CREDIT → CREATE JOB → PROVIDER ACCEPTS → BIND 2–5 INDEPENDENT SOURCES → FETCH + CONSENSUS → SETTLED / REJECTED / CONFLICTED`

An `OPEN` job can be cancelled by its client for a full refund if the provider never accepts. After the deadline, anyone can expire and refund any unresolved `OPEN`, `ACCEPTED`, or `EVIDENCE_BOUND` job. Before the deadline, either the client or provider can initiate evidence-based settlement. `SETTLED` transfers locked credits to the provider; `REJECTED`, `CONFLICTED`, `CANCELLED`, and `EXPIRED` refund the client. All terminal states are immutable.

## Consensus boundary

The leader and validators independently fetch every HTTPS URL and reconstruct exact content hashes, hash-match vector, authority list, duplicate-content flag, evidence-completeness gate, and four semantic delivery decisions. Acceptance requires exact equality of the complete report; there is no confidence tolerance that can cross a threshold.

## Security properties

- No caller supplies the verification outcome or confidence.
- Two or more distinct HTTPS authority domains are mandatory.
- Evidence content must match the precommitted SHA-256 hashes.
- Duplicate content fails closed.
- Either named party may trigger settlement before the deadline; only the provider can bind evidence.
- The client can cancel an unaccepted job, and anyone can refund an unresolved job after its deadline.
- Deadlines and terminal states prevent stale replay or repeated settlement.
- The proof root binds parties, terms, amount, deadline, fetched evidence, and decision.

## Commands

```powershell
genvm-lint check contracts/VerifiableServiceSettlement.py
genlayer network set studionet
genlayer deploy --contract contracts/VerifiableServiceSettlement.py
```

See `LIVE_PROOFS.md` for the matching deployed source and finalized lifecycle transactions.

Current StudioNet contract: https://explorer-studio.genlayer.com/address/0xedDb6FE1D0534FF78Af968397310749E540618b2. Run `node --test tests/security.test.mjs` and the GenLayer direct tests in `tests/direct/` to check the cancellation, expiry, and provider-settlement paths.
