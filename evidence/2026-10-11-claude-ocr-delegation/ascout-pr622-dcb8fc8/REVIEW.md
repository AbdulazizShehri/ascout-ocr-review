# Ascout #622 (UA-P06-T11B) — OCR delegation review by Claude (SELF-REVIEW)

- **Exact range:** `9520e020551cc7763bfd78c4c97a95a38fa93320..dcb8fc8686904703d6a9bdcd475db44bd69f4961` (#621 head .. T11B head)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/assurance/security/sentrdel-sarif-export.ts`. Excluded and reviewed separately: `tests/assurance-security-t11b.test.ts` (`default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid API or review service.
- **Independence:** **SELF-REVIEW.** Claude authored every line. Not an independent review.

## Findings (resolved before the reviewed head)

1. **Medium (correctness, found by real-component tests)** — the first design snapshotted whole T04 records, but real T04 observations share frozen sub-objects and the tree-only snapshot refuses them. Replaced by own-data-descriptor reads of exported fields only.
2. **Medium** — PARTIAL locations (path without both lines) were dropped; T04 keeps the path, so it is now exported without a region.
3. **Medium (security)** — backslash was not in the forbidden path class (escaping error). Fixed and tested.
4. **Medium (security/interop)** — a colon path (`C:x.ts`, `a:b/c`) would read as a drive or URI scheme and fail the T11A import. Refused; mutation re-allowing it fails the suite.
5. **Medium (OCR hardcoding rule)** — hardcoded `informationUri` removed.
6. **Test integrity** — an initial test fed T04 input that real T04 refuses; replaced by genuine T04 observations (`location: null` → ABSENT; dependency observation without rule).

**Open at dcb8fc8: High 0 · Medium 0.** Low (discarded): sort comparator duplicates earlier modules.

## Test file review (OCR-excluded)

Review-only SARIF and non-truth properties; T11A round trip as INFERENCE; unresolved rule naming; PARTIAL/ABSENT locations; determinism; refusals: empty, shared/duplicate, mixed source/attempt, >4096, missing entry, 7 promoted fields, total coverage, 8 bad paths, zero line, accessor (getter never runs), secret rule ID and path. All fixtures are real `normalizeSentrdelEvidenceV1` output.

**Mutation check:** 7 of 8 mutations fail the suite (kind→pass, promotion check, mixed-source check, duplicate check, canonical-truth flag, locations dropped, colon allowed). The survivor (accessor branch removed) is equivalent: descriptors never invoke getters, so an accessor reads as `undefined` and every field check still refuses it.

## Other checks

- Jev: `"noul":0.06` (leans no).
- Diffcipline (external policy, typecheck + T11B tests): **PASS**, 2 files, +290.
- Local: typecheck 0; 14 security test files, 271/271.
- E2E on built `dist`: `e2e-built-module.txt` (real SAST + dependency observations → review-only SARIF → T11A re-import as INFERENCE; promoted record refused).
- Production `npm audit`: 0.
- Exact-head CI attempt 1: Project CI 38167059347 success 6/6; Self Verification 38167059264 success.
- **UA-P06 §16 review condition: PENDING #619.**
