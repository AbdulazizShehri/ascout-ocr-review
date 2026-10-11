# Ascout #624 (UA-P06-T13) — OCR delegation review by Claude (SELF-REVIEW)

- **Exact range:** `27725cba7132bb981ceebc0719e0e6899149d564..65effa4902ebb3361c707296d8f73c23074abe26` (#623 head .. T13 head)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/assurance/security/sentrdel-remediation-retest.ts` (+158), `src/assurance/security/sentrdel-observation-read.ts` (+49). Excluded and reviewed separately: `tests/assurance-security-t13.test.ts` (+120, `default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid API or review service.
- **Independence:** **SELF-REVIEW.** Claude authored every line. Not an independent review.

## Findings

1. **Medium (test coverage, found by mutation testing)** — removing the retest-observation capability check went undetected; a real T04 secrets observation from another capability is now refused in the tests, and the mutant fails.

**Open at 65effa4: High 0 · Medium 0.**

## Design notes

The pinned donor has no retest lifecycle (its reconciler models Detected/Corroborated/Contested findings only); this contract is Ascout-native and derived from authorization §8 (`FIX_WITHOUT_RETEST != VERIFIED`) and §11 (`fix_without_new_evidence_presented_as_verified = 0`). Scope coverage requires an exact path or a parent directory followed by `/` (so `sr` and `src/app.tsx` do not cover `src/app.ts`); `.` covers nothing (fail closed).

## Test file review (OCR-excluded)

All four states; every incomplete reason individually; rule-less original; in-scope by file and by directory; determinism and binding to fix and retest evidence; refusals: fix at observed head, retest at another head, other capability (run and observation), old-head, other-attempt observations, run/observation mismatch, extra keys, invented coverage, secret fix ref, promoted original and retest observations, accessor (never invoked). All fixtures are real `normalizeSentrdelEvidenceV1` output.

**Mutation check:** 10/10 targeted mutations fail the suite (fix without retest closes, non-executed, partial coverage, unknowns, slashless scope prefix, unbound retest head, fix at observed head, foreign capability, re-observation ignored, verified flag).

## Other checks

- Jev: `"noul":0.09` (leans no).
- Diffcipline (external policy, typecheck + T13 tests): **PASS**, 3 files, +327.
- Local: typecheck 0; 16 security test files, 281/281.
- E2E on built `dist`: `e2e-built-module.txt` (five-step lifecycle walk-through).
- Production `npm audit`: 0.
- Exact-head CI attempt 1: Project CI 38168714937 success 6/6; Self Verification 38168714868 success.
- **UA-P06 §16 review condition: PENDING #619.**
