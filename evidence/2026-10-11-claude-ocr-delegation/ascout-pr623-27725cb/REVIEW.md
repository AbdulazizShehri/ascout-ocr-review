# Ascout #623 (UA-P06-T12) — OCR delegation review by Claude (SELF-REVIEW)

- **Exact range:** `dcb8fc8686904703d6a9bdcd475db44bd69f4961..27725cba7132bb981ceebc0719e0e6899149d564` (#622 head .. T12 head)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/assurance/security/sentrdel-reproduction-link.ts` (+126). Excluded and reviewed separately: `tests/assurance-security-t12.test.ts` (+86, `default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid API or review service.
- **Independence:** **SELF-REVIEW.** Claude authored every line. Not an independent review.

## Findings

**Open at 27725cb: High 0 · Medium 0.** Low (discarded, recorded as follow-up): the own-data-descriptor reader and non-promotion table duplicate T11B; extracting them would edit T11B inside this PR.

## Fidelity to the pinned donor

`crates/sentrdel-schema/src/evidence.rs` @ f5747319: `ReproductionMetadata { method, input_digest, notes }`; a reproduction input digest must equal a declared evidence input digest (`ReproductionInputDigestNotTrusted`). Ascout binds it to the observation's raw-evidence digest, additionally requires the declared reference and same source head, and omits free-text `notes` (secret-persistence risk). Runtime exploit proof is unsupported per the reproducibility-proof capability, so no executed/proven state exists.

## Test file review (OCR-excluded)

Linked/declared-not-supplied/none-declared states; no VERIFIED/REPRODUCED/PROVEN; determinism and identity binding; refusals: foreign digest, other reference, other head, unsolicited (message asserted), extra key, schema, empty and secret method, bad digest, non-record, 5 promoted observation fields, accessor (never invoked). Fixtures are real `normalizeSentrdelEvidenceV1` output.

**Mutation check:** 7/7 targeted mutations fail the suite (digest binding, unsolicited, reference, head, promotion check, reproduced flag, state promotion). The unsolicited mutant initially survived because the reference check also refuses; the test now asserts the specific reason.

## Other checks

- Jev: `"noul":0.06` (leans no).
- Diffcipline (external policy, typecheck + T12 tests): **PASS**, 2 files, +212.
- Local: typecheck 0; 15 security test files, 275/275.
- E2E on built `dist`: `e2e-built-module.txt`.
- Production `npm audit`: 0.
- Exact-head CI attempt 1: Project CI 38167809684 success 6/6; Self Verification 38167809663 success.
- **UA-P06 §16 review condition: PENDING #619.**
