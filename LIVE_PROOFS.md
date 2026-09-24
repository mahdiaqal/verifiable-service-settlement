# Live StudioNet proofs

## Liveness-corrected deployment (current)

- Contract: https://explorer-studio.genlayer.com/address/0xedDb6FE1D0534FF78Af968397310749E540618b2
- Deployment: https://explorer-studio.genlayer.com/tx/0x135485a819ef5a02d36f692faf5bdc1c4b70b90fe7b6a8c46252be964fe2bc78
- Demo-credit grant: https://explorer-studio.genlayer.com/tx/0xaf52f6f1e1cb017f8482083ef585da52011a7a85ee34f19bb2fbdacf37130376

The deployed source matches `contracts/VerifiableServiceSettlement.py` exactly after newline normalization. It contains `cancel_unaccepted`, `refund_expired`, and the two-party `verify_and_settle` authorization. The deployment and the three terminal-path transactions below reached `FINALIZED` with successful contract execution.

### Unaccepted cancellation

- Lock 40 credits: https://explorer-studio.genlayer.com/tx/0xc8d4baf2712f0338a994c6ee2f142ced8678047f8bcec0038c0e5940ae7682b9
- Client cancels and recovers 40: https://explorer-studio.genlayer.com/tx/0xa4f8e698ec26655555c7eddd385f4d81628bbb07c5e905b8529b3f3fe9658eed

The job ended `CANCELLED`, with a proof root, and the client's balance returned to 300 demo credits.

### Post-deadline refund

- Lock 50 credits: https://explorer-studio.genlayer.com/tx/0x5ab2858bf51eb8975637721e4e7888e96b400c625cb4c5e236341bd24afb4028
- Provider accepts: https://explorer-studio.genlayer.com/tx/0x0b62c75bb8c1ac68705af160b6ff5dc1285f3f1126836d4e9d5887862bc77b1d
- After deadline, provider calls `refund_expired` and the client recovers 50: https://explorer-studio.genlayer.com/tx/0x628d033a7c46476bcbb5d7cbebd7679d45b4014081cb6662dcfbb2ab9aa74baa

The accepted job ended `EXPIRED`, with proof root `2ef79ecea25a6a6dccc69edd86cc6ae6f86b2800804fcb339f5a1189c9df51f5`. The same refund method covers `OPEN` and `EVIDENCE_BOUND`; direct tests exercise all three unresolved states and replay rejection.

### Provider-initiated settlement before deadline

- Lock 60 credits: https://explorer-studio.genlayer.com/tx/0x022d477f2ea4331b8ed8d44c48b73d06060b5e0ac59c2b5b5a3df8b18872049d
- Provider accepts: https://explorer-studio.genlayer.com/tx/0x9f8f67ae40fe0d5c33189802451731199f2701f03650eed161a7ed40ba2b2868
- Provider binds RFC and IANA evidence: https://explorer-studio.genlayer.com/tx/0xe04e953403063a5bf2545dd0fd54a8280e10c992a2783b43cd60308a4789fe28 and https://explorer-studio.genlayer.com/tx/0x447c7b8ec070d166540ed8f813ecf9b20528d269627c341bbf43205cd165f6bf
- Provider calls `verify_and_settle`: https://explorer-studio.genlayer.com/tx/0xf6c520ec71b86169224dd261a5ac5a85cf66f9e18f3a3e6c87ed6d59b119b46d

The provider initiated the call without a client transaction. Validators independently fetched two distinct authorities; both SHA-256 commitments matched, duplicate content was false, and the four semantic decisions were true. The job ended `SETTLED`; the provider received 60 demo credits and proof root `24fcfe81ec2623e4bd35942117c7ec24ed23febd9cf4ece2ce48e01205394667`.

## Superseded deployment (pre-liveness fix)

- Previous contract: [`0xd6171a4157c453fDA1B8219c09156b310d9bdA24`](https://explorer-studio.genlayer.com/address/0xd6171a4157c453fDA1B8219c09156b310d9bdA24)
- Previous deployment: [`0xb1770f56...ad93c5`](https://explorer-studio.genlayer.com/tx/0xb1770f56c630d585cc02831abe50d6a277983fd285cf66360ed8d22039ad93c5)

The deployment executed successfully with five validator `AGREE` votes. Explorer source includes strict hexadecimal SHA-256 validation, contract-side HTTPS acquisition, exact validator report comparison, distinct-authority enforcement, duplicate-content rejection, and stateful credit settlement.

## Pre-release adversarial execution

The pre-release deployment intentionally exercised a hash-mismatch path. Validators fetched two independent sources, observed `[true, false]` hash matches, stored proof root `23aa3ab115f2ccf6b7eda5134c8f72f540f57fb90008a5ef8c176e951305ec9d`, moved the job to `CONFLICTED`, issued no provider credit, and refunded the client.

- Adversarial consensus transaction: [`0x734b8f1b...ac03d8`](https://explorer-studio.genlayer.com/tx/0x734b8f1bc9e2595f6a479902cd3f04abd69b62e3b6b0e300c764970a11ac03d8)

That run exposed acceptance of non-hexadecimal 64-character commitments. The current source retains the `_is_sha256` fix; neither older address is the liveness-corrected submission deployment.
