# ascout-ocr-review

Zero-cost, independent **Alibaba OpenCodeReview** runs for [Ascout](https://github.com/TheHalfMoon/Ascout) on free GitHub-hosted runners.

- The review model (`qwen3:4b-instruct-2507-q4_K_M`) runs **inside the runner** through Ollama on `127.0.0.1`. No inference API, no secrets, no paid compute.
- Pinned and verified: Ollama `v0.40.2` (SHA-256), model ID `0edcdef34593`, OCR `1.12.13` (build `fabbdb29`, npm lockfile), actions pinned by commit SHA.
- Manual `workflow_dispatch` only, `contents: read`, inputs validated as full SHAs.

## Modes

- `qualify` runs the model on a fixture with three planted defects (path-prefix traversal, off-by-one, shell command injection) and on a clean control, then scores both against a rule fixed **before** any run (`harness/ground-truth.json`).
- `review` reviews an exact `base..head` range of Ascout and uploads the OCR JSON (coverage, findings, run manifest) as an artifact.

## Non-claims

A completed run is not an approval. A review with zero findings is not proof of correctness. A review only counts as evidence for Ascout after the model has passed `qualify`, and Ascout's own governance decides how it is used.
