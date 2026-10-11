# Claude reviews in OCR delegation mode (2026-10-11)

Founder directive (2026-10-11): use the official Alibaba Open Code Review
(https://github.com/alibaba/open-code-review) in **delegation mode** with Claude
Code performing the review. Codex, paid APIs, DashScope, cubic, and other paid
review services are not used from this point.

Each `ascout-prNNN-<head>/` folder is bound to an exact commit range
(`range.txt`) and contains the OCR preview and rules, the full diff, Claude's
findings (`claude-review.json`), the human-readable record (`REVIEW.md`, which
also covers OCR-excluded files), and the Jev result.

**Labeling:** Claude-authored code reviewed by Claude is self-review. Reviews of
commits without a Claude attribution are not claimed as independent. Where a
governance gate requires an independent review (Ascout UA-P06 §16), the gate
is recorded as BLOCKED, not passed.

Earlier Codex evidence remains in `evidence/2026-10-11-codex/` as a historical record.
