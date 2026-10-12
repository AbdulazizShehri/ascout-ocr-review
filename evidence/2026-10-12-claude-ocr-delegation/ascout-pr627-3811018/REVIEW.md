# Ascout #627 (supplement S1) — §3 review record (SELF-REVIEW)

- **Exact range:** `5d2626f683b583dc987301def144d33f2be373d0..381101820c1c370c2f612e5921dc27bd915fda48` (main `5d2626f` merged into the branch by a normal merge; supplement text unchanged from `03a6019`)
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. 0 of 1 files selected (`UA_P06_T14_CLI_SURFACE_AMENDMENT_S1.md`, `unsupported_ext`); reviewed separately below.
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code under the effective review-model amendment (#619). No Codex, no paid service.
- **Independence:** **SELF-REVIEW.** Claude authored every line.

## Separate review of the OCR-excluded file

- **Facts re-verified on main `5d2626f`:** usage constants at `assurance-phase-qualification.test.ts` 37–44 (`toBe` at 93), `assurance-phase-recovery-qualification.test.ts` 36–43 (`toBe` at 87), `assurance-review-p03-t15.test.ts` 252–260. All match the text.
- **Necessity and sufficiency proven:** on T14 branch `4182b71` plus exactly the three S1 lines, all 13 CLI-surface test files pass (67/67): `assurance-security-t14`, `assurance-check-compatibility`, `assurance-test-cli-test-plan`, the three S1 sentinels, `cli-format.contract`, `assurance-test-phase-closeout`, `assurance-phase-p04-qualification`, `assurance-review-p03-t14`, `agent-integration-admission.contract`, `changed-command-surface-override.integration`, `t106-environment-publication.integration`. Without the lines, exactly the three S1 sentinels fail.
- **Scope:** only one identical line per file; no weakening; no check/review/test behavior change; no new option or command.

**Open: High 0 · Medium 0.**

## Other checks

- Jev (jev-1.13.0): `"noul":0.13` (leans no).
- Exact-head CI attempt 1: Self Verification 38186789933 success; Project CI 38186789914 success 6/6.
- Documentation only; no credentials.
