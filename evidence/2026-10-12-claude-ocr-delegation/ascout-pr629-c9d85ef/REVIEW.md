# Ascout #629 (UA-P06-T14) — §3 review record (SELF-REVIEW)

- **Exact range:** `d1184eabd7c94cf5e8c941647a842a44e94edc90..c9d85ef8469fa43a4e608f9bd0179bfa3d83efbd`
- **OCR:** open-code-review v1.12.13 (fabbdb29), official delegation mode. Selected: `src/cli.ts` (+37/-5), `src/assurance/security/security-command.ts` (+74). Excluded and reviewed separately: `README.md` and six test files (`unsupported_ext` / `default_path`).
- **Reviewer:** Claude (claude-opus-5-5) via Claude Code. No Codex, no paid service.
- **Independence:** **SELF-REVIEW.** Claude authored every line.

## Findings

**Open: High 0 · Medium 0.** Noted (intentional, not a check/review/test change): the `--format` refusal message for `init`/`doctor` now lists `security`; same refusal and exit code 2.

## Scope versus the effective amendments (#625 decisions A and B, #627 S1)

- One command, `security [--format json|terminal]`; any other option refused; `cyber`/`assure` stay refused.
- NOT_RUN with exit 1; never a pass; the report source imports no fs/net/process modules and reads no clock.
- Sentinel edits exactly as authorized: one usage line in four pins; `"security"` removed from three refused lists and one invalid-argv list. Removed negatives replaced by stronger positive tests (`assurance-security-t14.test.ts`, 7 tests).

## Evidence

- **E2E on built CLIs (main `d1184ea` vs T14) on a fixture repo** (`e2e-built-cli.txt`): `review` and `test` in json and terminal formats are byte-identical with the same exit codes. Usage-error stderr differs only by the authorized usage line and message. `security` exits 1 with NOT_RUN, `security_pass: false`, engine not executed, and the fixture tree is unchanged.
- **Mutation check:** 7/7 mutations fail the tests (exit 0, security_pass true, outcome PASS, extra format, usage line removed, JSON to stderr, `cyber` admitted).
- **Diffcipline** (external policy, typecheck + 7 CLI test files): PASS, 9 files, +234.
- **Full local suite at the T16 tip** (includes T14): 2221 passed; the 10 failures are 9 local Git-spawn timeouts and one Windows `tar` invocation (`cli.smoke`, `drift`, `git-diff`, `git-tree-digest`, `npm-package-content`, `t107`), all known local-host issues that pass in CI.
- **Jev:** `"noul":0.09`.
- **Exact-head CI attempt 1:** Project CI 38189162539 success 6/6; Self Verification 38189162505 success.
