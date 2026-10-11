# Ascout #621 (UA-P06-T11A) — OCR delegation review by Claude (SELF-REVIEW)

- **Exact range:** `9d805a9f56963093301011e6a57f5e9d48593361..9520e020551cc7763bfd78c4c97a95a38fa93320` (#620 head .. T11A head)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/assurance/security/sentrdel-sarif-import.ts` (+205). Excluded and reviewed separately: `tests/assurance-security-t11a.test.ts` (+108, `default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid API or review service.
- **Independence:** **SELF-REVIEW.** Claude authored every line. Not an independent review.

## Findings

1. **Medium (fidelity/security)** — result-message validation missed C1 control characters (U+0080–U+009F, e.g. U+009B CSI terminal escape) that the donor's `char::is_control` rejects. Fixed in 2eb3df1; test added in 9520e02; a mutation re-allowing C1 fails the suite.

**Open at 9520e02: High 0 · Medium 0.**

## Fidelity to the pinned donor

`crates/sentrdel-engine/src/adapter.rs` @ f5747319 (`adapt_sarif`, `validate_identifier`, `validate_result_text`, `normalize_repo_relative_path`, `MAX_ENGINE_*`): version 2.1.0 only; 64 runs, 4096 results, 64 locations; identifier/location/text byte caps; semanticVersion→version and text→markdown fallbacks; required ruleId and message; physicalLocation required; uriBaseId refused; path decoding and refusal rules; results are Inference-class. **Documented deviations:** (a) no workspace, so the donor's existing-prefix/symlink check is not performed and `path_existence_verified: false`; (b) stricter: `level` must be a SARIF 2.1.0 level; secret-shaped and self-attesting text refused.

## Test file review (OCR-excluded)

Inference-only mapping and frozen output; kind=pass/suppression/baseline ignored; empty import not clean; donor fallbacks; 14 refused URIs plus uriBaseId, logical-only, zero line; digest binding and tamper; bounds (runs, results, locations, bytes); identity, text, level, and secret refusals; determinism. Mutation check: 7 targeted mutations (digest binding, traversal, uriBaseId, absolute/scheme, message secret scan, epistemic promotion, C1 controls) each fail the suite.

## Other checks

- Jev: `"noul":0.1` (leans no).
- Diffcipline (external policy, typecheck + T11A tests): **PASS**, 2 files, +313.
- Local: typecheck 0; 13 security test files, 266/266.
- E2E on built `dist`: `e2e-built-module.txt` (multi-run CodeQL/Semgrep log; pass-kind suppressed result stays inference; tampered SARIF refused).
- Production `npm audit`: 0.
- Exact-head CI attempt 1: Project CI 38162370349 success 6/6; Self Verification 38162370359 success.
- **UA-P06 §16 review condition: PENDING #619.**
