# Codex independent-review evidence (2026-10-11)

Raw artifacts for the owner-authorized qualification of the OpenAI Codex CLI as an independent reviewer in Alibaba OpenCodeReview delegation mode, and for the resulting Ascout PR reviews. Summaries are in PR #4 and in TheHalfMoon/Ascout PR comments.

- Codex CLI `0.162.0-alpha.2`, ChatGPT subscription auth (no API key), model `gpt-6.1-sol`.
- OCR `v1.12.13 (fabbdb29)` delegation mode: `ocr delegate preview` / `ocr delegate rule` outputs are included.
- `qualification/attempts-1-2/`: attempt 1 (INVALID: sandbox could not run git; `codex-*`), attempt 2 (planted 3/3; true-positive clean comment on the defective v1 control; `codex2-*`).
- `qualification/attempt-3/`: run on the pre-registered clean-control v2 (`de86a53`): `PASS_AUTOMATIC_CRITERIA`. `*.adapted.json` wrap Codex output for `harness/score.py` and are labeled as not being OCR run manifests.
- `ascout-pr-reviews/prNNN/`: per-PR `range.txt` (base and exact head), OCR selection and rules, full diff, the exact prompt, Codex JSON events, and output.
- `*.stderr.txt` files contain only Codex runtime logs (including an MCP OAuth challenge header without credentials); no tokens are present.
