You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad..a77d51e99796607e18784b82d87185874a4333ec
Pull request title (context only): docs(notices): record Sentrdel reference-only provenance
Changed files: THIRD_PARTY_NOTICES.md

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, and whether tests keep their assertion strength.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (0 reviewable / 1 total)

- mode: range
- from: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- to: a77d51e99796607e18784b82d87185874a4333ec
- merge_base: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- total_insertions: 13
- total_deletions: 1

~~- `THIRD_PARTY_NOTICES.md` [modified] +13/-1 (excluded: unsupported_ext)~~

## OCR review rules
(no OCR rule groups)

## Diff
```diff
diff --git a/THIRD_PARTY_NOTICES.md b/THIRD_PARTY_NOTICES.md
index 449b24a..9121329 100644
--- a/THIRD_PARTY_NOTICES.md
+++ b/THIRD_PARTY_NOTICES.md
@@ -143,4 +143,16 @@ This file does not replace any third-party license text or attribution that a fu
 - Phases admitted: ARTEMIS-A0 through ARTEMIS-A12 closed canonically; A13 gates recorded in `docs/mobile/artemis-a13-release.md`
 - Donor telemetry: off by default; no telemetry destination admitted
 - Runtime authority: none granted by source presence or by release admission
-- Provenance record: `docs/mobile/artemis-a0-provenance.json`
\ No newline at end of file
+- Provenance record: `docs/mobile/artemis-a0-provenance.json`
+## Donor characterization — TheHalfMoon/Sentrdel (UA-P06)
+
+- Upstream: `https://github.com/TheHalfMoon/Sentrdel` (same GitHub owner account as Ascout; this entry makes no statement about legal copyright ownership)
+- Pinned commit: `f5747319a50831ef7cee983d253c0ca5503c9a64` ("Merge PR #333: make Sentrdel developer-first and adoption-ready", 2026-09-16)
+- Pinned tree: `0d70de477fa403a416a8cff5576498e4c59a1689`
+- License: Apache-2.0 (root `LICENSE`, blob `45d3d38717ab6e5fd41a53a9b14184d0e93f1007`); no nested license file in the selected paths
+- Notice material: none at the pin (no `NOTICE` file; selected source files carry no copyright headers), so no notice text is carried
+- Use type: reference-only characterization (`SENTRDEL_INTEGRATION_MODES = ["REFERENCE_ONLY"]`). Ascout re-expresses observed rule identifiers, capability semantics, and path classifications in its own TypeScript; no Sentrdel source files are copied or vendored
+- Ascout paths: `src/assurance/security/sentrdel-*.ts` and their tests
+- Repository visibility: recorded as public at pin time; private as of 2026-10-10, so third parties may be unable to inspect the pinned source
+- Runtime authority: none; Sentrdel output enters only through the external-engine adapter boundary as observations, never as Ascout assurance
+- Provenance record: `src/assurance/security/sentrdel-source-pin.ts` (`provenance:sentrdel-pin-f5747319a50831ef7cee983d253c0ca5503c9a64`)
```

## Full file at head: THIRD_PARTY_NOTICES.md
```
    1| # Third-Party Notices
    2| 
    3| **Status:** T086 exact-version dependency license/provenance review  
    4| **Scope:** direct dependencies intentionally selected for Ascout M1, bound to the current committed manifest and lockfile.
    5| 
    6| This file records the exact direct third-party packages selected by Ascout and the evidence used to bind those selections to the committed lockfile. Exact transitive versions, registry locations, integrity digests, and license metadata are recorded in `package-lock.json` where npm provides those fields.
    7| 
    8| ## Current candidate binding
    9| 
   10| T086 revalidated this ledger against canonical `main` at `a9bae09a71b4ff92097182a8d97f5ff6a0511603`.
   11| 
   12| - `package.json` blob: `e5d99fcd1bb87fa3adec2629d949bde933000bf7`
   13| - `package-lock.json` blob: `e51f0bddb953235c1a391718eabfab5a6c680832`
   14| - Product runtime dependency count: 1 (`cross-spawn@7.0.6`)
   15| - Direct development dependency count: 6 (`@types/node`, `@vitest/coverage-v8`, `jest`, `typescript`, `vite`, `vitest`)
   16| - Direct manifest/lockfile reconciliation: complete; no direct dependency is omitted from this notice ledger.
   17| 
   18| The committed npm lockfile is the canonical machine-readable graph for this candidate. The T086 review does not upgrade dependencies, regenerate the lockfile, alter package identity, publish to npm, or claim that a point-in-time security audit is permanent.
   19| 
   20| ## Lock generation evidence
   21| 
   22| - Evidence branch: `evidence/t003-lockgen-2026-08-22` (the date component is the Asia/Riyadh local date; the corresponding GitHub Actions timestamps are on 2026-08-21 UTC).
   23| - Evidence commit containing the generated lockfile: `81e2850e06a097abed5a7566aded39fceb330800`
   24| - Original generated `package-lock.json` blob: `751fdf89c10d26a1875844626ad6c336b28d051b`
   25| - GitHub Actions generation run: `32535056565`
   26| - Runner OS: Ubuntu 24.04
   27| - Node: `22.0.0`
   28| - npm resolver: `10.9.4`
   29| - Generation command: `npm install --package-lock-only --ignore-scripts --audit=false --fund=false`
   30| - Reproduction check: `npm ci --ignore-scripts --audit=false --fund=false` — PASS
   31| - Exact direct-resolution check — PASS
   32| - `npm ls --all` — exited successfully; its tree truthfully reports platform-, peer-, and engine-inapplicable optional dependencies as `UNMET OPTIONAL DEPENDENCY` rather than treating them as required install failures.
   33| - Tool execution on Node 22.0.0: TypeScript `6.0.3`, Vite `6.4.3`, Vitest `4.1.10` — PASS
   34| - Generation-time security check: `npm audit --package-lock-only --audit-level=high` reported `found 0 vulnerabilities`.
   35| 
   36| ### Node 22.0.0 engine-strict verification
   37| 
   38| A follow-up evidence run `32535678363` used the same package manifest and unchanged lockfile blob on Node `22.0.0` with npm `10.9.4` and added an engine-strict installation gate:
   39| 
   40| - `npm ci --engine-strict --ignore-scripts --audit=false --fund=false` — PASS
   41| - `@napi-rs/lzma-linux-x64-gnu@1.5.1`, an optional dependency of `rollup@4.62.5` whose own engine range starts at Node 22.20, was omitted by npm on Node 22.0.0 as an inapplicable optional dependency.
   42| - The workflow asserted that this optional package was absent after the engine-strict install.
   43| - Vite `6.4.3` executed on Node `22.0.0` after that install — PASS.
   44| - Vitest `4.1.10` executed on Node `22.0.0` after that install — PASS.
   45| - The follow-up audit again reported `found 0 vulnerabilities` for the resolved lockfile graph.
   46| 
   47| The stricter engine range of an omitted optional package therefore does not redefine Ascout's Node `>=22` support floor. The evidence above is deliberately scoped to the tested Ubuntu x64 environment and does not claim an untested platform result.
   48| 
   49| Security/audit results are evidence for the specific resolved graph at the cited runs; they are not permanent security claims.
   50| 
   51| ## T086 license/provenance reconciliation
   52| 
   53| All seven direct packages declared by the current candidate are represented below at their exact locked versions. The current direct set contains Apache-2.0 and MIT licenses only. No direct copyleft, source-available, non-commercial, field-of-use, database, or data-license restriction was identified in the manifest/lockfile evidence reviewed for T086.
   54| 
   55| This conclusion is scoped to the exact direct package versions below. Transitive packages remain separately represented by the committed lockfile and may use other permissive SPDX licenses. A future dependency/version change requires a fresh provenance/license reconciliation before release claims are updated.
   56| 
   57| ## Direct dependencies
   58| 
   59| ### `cross-spawn` 7.0.6
   60| 
   61| - Role: product runtime dependency
   62| - License: MIT
   63| - Upstream: `moxystudio/node-cross-spawn`, tag `v7.0.6`
   64| - Registry tarball: `https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz`
   65| - SRI: `sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==`
   66| 
   67| ### `@types/node` 22.20.1
   68| 
   69| - Role: development-only Node.js type declarations aligned to the Node 22 support floor
   70| - License: MIT
   71| - Upstream: `DefinitelyTyped/DefinitelyTyped`, package path `types/node`
   72| - Registry tarball: `https://registry.npmjs.org/@types/node/-/node-22.20.1.tgz`
   73| - SRI: `sha512-EANqOCF9QFyra+4pfxUcX9STKJpCLjMbObVzljIJomAWSnuSIEAvyzEU53GaajbXJEgdh0iEcPL+DGvpUd4k1Q==`
   74| 
   75| ### `@vitest/coverage-v8` 4.1.10
   76| 
   77| - Role: development-only V8 coverage provider used by the Vitest integration and changed-code exercise tests
   78| - License: MIT
   79| - Upstream: `vitest-dev/vitest`, tag `v4.1.10`, package path `packages/coverage-v8`
   80| - Registry tarball: `https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.10.tgz`
   81| - SRI: `sha512-IM49HmthevbgAO4anp1hwtoT9wYe59w0LR00gr+eagHE+ZJ5lK4sLPeO0ubgoJcwLk6dehU3R24N+FbEEKDc8g==`
   82| 
   83| ### `jest` 30.4.2
   84| 
   85| - Role: development-only Jest runner used to qualify Ascout's supported Jest integration
   86| - License: MIT
   87| - Upstream: `jestjs/jest`, tag `v30.4.2`
   88| - Registry tarball: `https://registry.npmjs.org/jest/-/jest-30.4.2.tgz`
   89| - SRI: `sha512-Yi1jqNC/Oq0N4hBgNH/YvBpP1P57QqundgytzYqy3yqAa7NZPNjSoi4SGbRAXDMdBzNE6xBCi5U7RgfrvMEUVQ==`
   90| 
   91| ### `typescript` 6.0.3
   92| 
   93| - Role: development-only compiler/typechecker
   94| - License: Apache-2.0
   95| - Upstream: `microsoft/TypeScript`, tag `v6.0.3`
   96| - Registry tarball: `https://registry.npmjs.org/typescript/-/typescript-6.0.3.tgz`
   97| - SRI: `sha512-y2TvuxSZPDyQakkFRPZHKFm+KKVqIisdg9/CZwm9ftvKXLP8NRWj38/ODjNbr43SsoXqNuAisEf1GdCxqWcdBw==`
   98| 
   99| ### `vite` 6.4.3
  100| 
  101| - Role: development-only peer/runtime substrate selected for Vitest while preserving the Ascout Node `>=22` floor
  102| - License: MIT
  103| - Upstream: `vitejs/vite`, tag `v6.4.3`, package path `packages/vite`
  104| - Registry tarball: `https://registry.npmjs.org/vite/-/vite-6.4.3.tgz`
  105| - SRI: `sha512-NTKlcQjlAK7MlQoyb6LgaqHc8sso/pVyUJYWMws3jg21uTJw/LddqIFPcPqP6PzpgbIcZyKI85sFE4HBrQDA8A==`
  106| 
  107| ### `vitest` 4.1.10
  108| 
  109| - Role: development-only test runner
  110| - License: MIT
  111| - Upstream: `vitest-dev/vitest`, tag `v4.1.10`, package path `packages/vitest`
  112| - Registry tarball: `https://registry.npmjs.org/vitest/-/vitest-4.1.10.tgz`
  113| - SRI: `sha512-R9jUTe5S4Qb0HCd4TNqpC7oGcrMssMRGXLW80ubjWsW9VH5GF8y1Y0SFLY9AbqSk6nt0PnOx4H4WNJYZ13GUPw==`
  114| 
  115| ## Transitive dependencies
  116| 
  117| `package-lock.json` is the canonical machine-readable record for the exact resolved transitive graph used by this revision, including registry `resolved` URLs, SRI `integrity` values, and license metadata where npm records it. Optional entries can legitimately remain recorded even when npm omits them on a particular platform or Node version.
  118| 
  119| The T086 review does not treat process isolation, development-only status, or npm registry availability as a substitute for license terms. It also does not assume that a permissive direct package makes every possible future bundled artifact attribution-free. The T082 package-content gate proves the current Ascout tarball surface separately; any future bundling/vendor change must re-evaluate redistribution and notice obligations.
  120| 
  121| This file does not replace any third-party license text or attribution that a future packaged distribution is legally required to carry.
  122| 
  123| ## Donor snapshot — google/artemis (ARTEMIS A0)
  124| 
  125| - Upstream: `https://github.com/google/artemis`
  126| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  127| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  128| - License: Apache-2.0
  129| - Ascout paths: `vendor/google-artemis/**` plus separately reviewed adapters
  130| - Use type: copied + adapted, Class C provenance
  131| - Snapshot content: complete repository snapshot at the exact commit (796 blob paths)
  132| - Notice preservation: donor LICENSE, copyright headers, and notice material preserved inside the immutable snapshot; no modifications inside the snapshot
  133| - Runtime authority: none granted by source presence; activation requires separate phased authorization and qualification
  134| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
  135| 
  136| ## Donor snapshot — google/artemis (ARTEMIS A13 release admission)
  137| 
  138| - Upstream: `https://github.com/google/artemis`
  139| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  140| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  141| - License: Apache-2.0
  142| - Release scope: contract, adapter, evidence, and documentation layers under `vendor/google-artemis/**`, `src/assurance/engines/mobile-artemis/**`, `python/ascout_mobile_bridge/**`, `schemas/mobile-artemis/**`, `docs/mobile/**`
  143| - Phases admitted: ARTEMIS-A0 through ARTEMIS-A12 closed canonically; A13 gates recorded in `docs/mobile/artemis-a13-release.md`
  144| - Donor telemetry: off by default; no telemetry destination admitted
  145| - Runtime authority: none granted by source presence or by release admission
  146| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
  147| ## Donor characterization — TheHalfMoon/Sentrdel (UA-P06)
  148| 
  149| - Upstream: `https://github.com/TheHalfMoon/Sentrdel` (same GitHub owner account as Ascout; this entry makes no statement about legal copyright ownership)
  150| - Pinned commit: `f5747319a50831ef7cee983d253c0ca5503c9a64` ("Merge PR #333: make Sentrdel developer-first and adoption-ready", 2026-09-16)
  151| - Pinned tree: `0d70de477fa403a416a8cff5576498e4c59a1689`
  152| - License: Apache-2.0 (root `LICENSE`, blob `45d3d38717ab6e5fd41a53a9b14184d0e93f1007`); no nested license file in the selected paths
  153| - Notice material: none at the pin (no `NOTICE` file; selected source files carry no copyright headers), so no notice text is carried
  154| - Use type: reference-only characterization (`SENTRDEL_INTEGRATION_MODES = ["REFERENCE_ONLY"]`). Ascout re-expresses observed rule identifiers, capability semantics, and path classifications in its own TypeScript; no Sentrdel source files are copied or vendored
  155| - Ascout paths: `src/assurance/security/sentrdel-*.ts` and their tests
  156| - Repository visibility: recorded as public at pin time; private as of 2026-10-10, so third parties may be unable to inspect the pinned source
  157| - Runtime authority: none; Sentrdel output enters only through the external-engine adapter boundary as observations, never as Ascout assurance
  158| - Provenance record: `src/assurance/security/sentrdel-source-pin.ts` (`provenance:sentrdel-pin-f5747319a50831ef7cee983d253c0ca5503c9a64`)
```
