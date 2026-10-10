# ascout-ocr-review

Zero-cost, independent **Alibaba OpenCodeReview** runs for [Ascout](https://github.com/TheHalfMoon/Ascout) on free GitHub-hosted runners.

- **Providers.** `dashscope-intl` / `dashscope-cn`: Alibaba Cloud Model Studio (Qwen) through OCR's OpenAI-compatible provider. The key comes only from the `DASHSCOPE_API_KEY` repository secret, is read via `api_key_cmd`, and is never written to OCR's config; every run has a hard `--max-tokens-budget`. `ollama-local`: model inside the runner on `127.0.0.1`, no secrets.
- **Egress control.** In `review` mode a pinned, checksum-verified gitleaks scans the exact range first; any finding stops the run before content reaches the provider.
- **Cost control is yours.** Enable Model Studio's "Free quota only" setting so the service stops when the free quota is used up instead of switching to pay-as-you-go.
- Pinned and verified: Ollama `v0.40.2` (SHA-256), model ID `0edcdef34593`, OCR `1.12.13` (build `fabbdb29`, npm lockfile), actions pinned by commit SHA.
- Manual `workflow_dispatch` only, `contents: read`, inputs validated as full SHAs.

## Modes

- `qualify` runs the model on a fixture with three planted defects (path-prefix traversal, off-by-one, shell command injection) and on a clean control, then scores both against a rule fixed **before** any run (`harness/ground-truth.json`).
- `review` reviews an exact `base..head` range of Ascout and uploads the OCR JSON (coverage, findings, run manifest) as an artifact.

## Non-claims

A completed run is not an approval. A review with zero findings is not proof of correctness. A review only counts as evidence for Ascout after the model has passed `qualify`, and Ascout's own governance decides how it is used.
