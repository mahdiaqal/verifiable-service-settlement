# Live StudioNet proofs

- Final contract: [`0xd6171a4157c453fDA1B8219c09156b310d9bdA24`](https://explorer-studio.genlayer.com/address/0xd6171a4157c453fDA1B8219c09156b310d9bdA24)
- Final deployment: [`0xb1770f56...ad93c5`](https://explorer-studio.genlayer.com/tx/0xb1770f56c630d585cc02831abe50d6a277983fd285cf66360ed8d22039ad93c5)

The deployment executed successfully with five validator `AGREE` votes. Explorer source includes strict hexadecimal SHA-256 validation, contract-side HTTPS acquisition, exact validator report comparison, distinct-authority enforcement, duplicate-content rejection, and stateful credit settlement.

## Pre-release adversarial execution

The pre-release deployment intentionally exercised a hash-mismatch path. Validators fetched two independent sources, observed `[true, false]` hash matches, stored proof root `23aa3ab115f2ccf6b7eda5134c8f72f540f57fb90008a5ef8c176e951305ec9d`, moved the job to `CONFLICTED`, issued no provider credit, and refunded the client.

- Adversarial consensus transaction: [`0x734b8f1b...ac03d8`](https://explorer-studio.genlayer.com/tx/0x734b8f1bc9e2595f6a479902cd3f04abd69b62e3b6b0e300c764970a11ac03d8)

That run exposed acceptance of non-hexadecimal 64-character commitments. The final source fixes this with `_is_sha256`; the pre-release address is not the submission deployment.
