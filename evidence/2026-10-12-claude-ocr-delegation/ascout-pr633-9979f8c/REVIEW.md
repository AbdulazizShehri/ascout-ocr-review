# Ascout #633 (#626 maintenance) — §3 review record (SELF-REVIEW)

- **Exact range:** `ea93553a5423fd47f12a6bf282820dd199b994d4..9979f8c8166493a63592e3b4f33cf96eb3933309`
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: 9 source files under `src/assurance/security/`. Excluded and reviewed separately: `tests/assurance-security-code-unit-order.test.ts` (`default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid service.
- **Independence:** **SELF-REVIEW.** Claude authored every line.

## Behavior preservation

- Comparator: all seven replaced functions were three-way UTF-16 code-unit comparisons; the shared `compareCodeUnitsV1` is the same function. Imported under each file's existing local name, so call sites are unchanged.
- Readers: the shared ID pattern, check order, non-promotion table (identical keys in identical order, so the first-reported failing key is unchanged), and every error message are byte-identical to the replaced code. T11B's secret-message wording differs from the shared helper, so that helper stays local.
- **No existing test file changed.** 20 security test files, 309/309 pass, plus the new comparator contract test (2/2).
- **Both security benchmarks** on a built `main` vs this head: **byte-identical** JSON (`benchmarks-main.json` = `benchmarks-refactor.json`, 4001 bytes).
- **Mutation:** an inverted shared comparator fails 5 test files; equal-not-zero and `localeCompare` variants fail the new contract test.

**Open: High 0 · Medium 0.**

## Other checks

- Jev: `"noul":0.26`. Diffcipline (external policy, typecheck + 9 affected test files): PASS, 10 files, +44/−64.
- Exact-head CI attempt 1: Project CI 38194214655 success 6/6; Self Verification 38194214635 success.
