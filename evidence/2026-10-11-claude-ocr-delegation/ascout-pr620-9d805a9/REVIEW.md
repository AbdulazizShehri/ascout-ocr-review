# Ascout #620 (UA-P06-T10) — OCR delegation review by Claude (SELF-REVIEW)

- **Exact range:** `c5e7fe0f97082b63fb9634116396e7a2295930f6..9d805a9f56963093301011e6a57f5e9d48593361` (#606 head .. T10 head)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/assurance/security/sentrdel-invariant-regression.ts` (+232). Excluded and reviewed separately: `tests/assurance-security-t10.test.ts` (+152, `default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid API or review service.
- **Independence:** **SELF-REVIEW.** Claude authored every line. Not an independent review.

## Findings (resolved before the reviewed head)

1. **Medium (security)** — `invariant_id` is copied into the output but was not secret-scanned; an AKIA-shaped key fits the ID pattern (hard-zero `secret_plaintext_in_persisted_artifact`). Fixed: IDs get the shared secret and self-attestation scan; test added; mutation removing the scan fails the suite.
2. **Medium (OCR rule: nested ternary)** — two nested ternaries replaced by named helpers.

**Open at 9d805a9: High 0 · Medium 0.** Low (discarded): code-unit comparator duplicates the T09C pattern.

## Semantics checked against the pinned donor

`crates/sentrdel-review/src/regression/model.rs` @ f5747319: all 8 `FROZEN_INVARIANT_TRANSITIONS` transcribed; where the donor admits two dispositions the coverage disposition is chosen. Transitions outside the table, redefinitions, and NOT_APPLICABLE stay UNKNOWN. Non-COVERED coverage is effective UNKNOWN.

## Test file review (OCR-excluded)

Covers every frozen transition, all six degraded coverage states, coverage gain, unknown/NA/redefinition, base-only/candidate-only, determinism and order independence, frozen output, no-promotion flags, 25 fail-closed rejections, and getter non-execution. Mutation check: 5 targeted mutations (coverage ignored, S>U as UNCHANGED, removal as UNCHANGED, same-revision check removed, ID secret scan removed) each fail the suite.

## Other checks

- Jev: `"noul":0.12` (uncertainty lost or secret persisted → leans no).
- Diffcipline (external policy `diffcipline-t10.toml`, verification typecheck + T10 tests): **PASS**, 2 files, +384.
- Local: typecheck 0 errors; 12 security test files, 259/259.
- E2E on the built `dist` module: `e2e-built-module.txt` (regression, coverage loss on timeout, removal, improvement without remediation verification, same-revision refusal).
- Production `npm audit`: 0. Secret-shaped literals added: 0.
- Exact-head CI attempt 1: Project CI 38161487818 success 6/6; Self Verification 38161487766 success.
- **UA-P06 §16 review condition: PENDING** amendment #619 (founder exact-head approval).
