You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: 8d609796f7ff0a940831d395cc1a1cc873899f94..5ff987260cd14896f56b49390c978d46b7f95450
Pull request title (context only): test(docs): enforce notices completeness and clarify current CLI semantics
Changed files: README.md,THIRD_PARTY_NOTICES.md,tests/third-party-notices.test.ts

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, whether tests keep their assertion strength, and whether documentation claims are accurate.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (0 reviewable / 3 total)

- mode: range
- from: 8d609796f7ff0a940831d395cc1a1cc873899f94
- to: 5ff987260cd14896f56b49390c978d46b7f95450
- merge_base: 8d609796f7ff0a940831d395cc1a1cc873899f94
- total_insertions: 63
- total_deletions: 3

~~- `README.md` [modified] +4/-0 (excluded: unsupported_ext)~~
~~- `THIRD_PARTY_NOTICES.md` [modified] +20/-3 (excluded: unsupported_ext)~~
~~- `tests/third-party-notices.test.ts` [added] +39/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- tests/third-party-notices.test.ts

#### Content

#### Obvious Typos or Spelling Errors
- Spelling errors in variable names, function names, component names, or Props property names
- Strings in log or error messages containing spelling errors that affect readability

#### Dead Code
- Code blocks that will never be executed (e.g., branches where the condition is always false, code after a return statement)
- Variables that are declared but never read or referenced
- Large blocks of commented-out code (with no apparent intent to retain)

#### Code Quality Checks
- **Duplicate Code**: Check for common logic that can be extracted
- **Code Comments**: Complex business logic should have clear explanatory comments (avoid commenting obvious code)
- **Hardcoding**: Business-related hardcoded strings are prohibited, especially URL paths and business numbers; simple UI text may be relaxed
- **Variable Declarations**: Using `var` is strictly prohibited; use `let` or `const`
- **Equality Comparisons**: Using `==` and `!=` is prohibited; use strict equality `===` and `!==`
- **TypeScript Types**: Avoid using `any` type; if necessary, provide a comment explaining the reason
- **Null Checks**: Perform null checks when accessing values or destructuring to avoid null pointer exceptions
- **Ternary Expressions**: Nested ternary expressions are not allowed

#### React Best Practices
- **Hooks Usage**: Verify compliance with Hooks rules (only call at the top level, only call in React functions)
- **State Management**: Ensure state is placed at the appropriate level; avoid unnecessary state lifting
- **Side Effect Handling**: Verify useEffect correctly handles dependencies and cleanup functions
- **Performance Optimization**: Verify proper use of React.memo, useMemo, useCallback (based on performance analysis; avoid over-optimization)
- **Render Side Effects**: Side effects in React component render methods are strictly prohibited (e.g., API calls, DOM manipulation)
- **Inline Styles**: Avoid using inline `style` attributes, except for dynamic styles
- **Inner Components**: Declaring new components inside a component is prohibited; use render methods instead (e.g., `renderItem`, not `<Item/>`)

#### Async Handling Standards
- **Error Handling**: Async functions must include proper error handling with user-friendly error messages
- **Prefer async/await**: Prefer async/await over Promises; callback hell is prohibited
- **Async in Loops**: Distinguish between independent async operations (use `Promise.all` for parallelism) and dependent async operations (use sequential execution); prefer `Promise.all` for performance

#### Code Security Checks
- **XSS Protection**: Verify that user input is properly escaped
- **innerHTML Safety**: Using innerHTML to directly insert user input is prohibited; use textContent or apply XSS protection
- **Code Injection Protection**: Using eval(), Function() constructor, and string argument forms of setTimeout/setInterval is strictly prohibited
- **Dangerous Methods**: Using document.write() is prohibited as it causes page reflow and security issues
- **Sensitive Information**: Check whether API keys or sensitive data are exposed
- **Prototype Chain Safety**: Modifying native object prototypes (e.g., Array.prototype, Object.prototype) is prohibited

## Diff
```diff
diff --git a/README.md b/README.md
index 849d49d..9d7842e 100644
--- a/README.md
+++ b/README.md
@@ -93,8 +93,12 @@ The last command prints usage and exits with a usage error because a command is
 ascout init
 ascout doctor
 ascout check [--allow-changed-command-surface] [--format json|agent]
+ascout review [--format json|terminal]
+ascout test [--profile quick|standard|deep|release] [--format json|terminal]
 ```
 
+**Current command semantics (v0.1.0):** `ascout check` executes supported local verification tasks and produces an evidence receipt. `ascout review` presently reports review scope or unavailable review execution; it does **not** run a code-review engine. `ascout test` presently creates a test plan; it does **not** execute that plan. Both `review` and `test` can currently exit with code 0 even though no review or advanced test execution took place. That exit status is **not an assurance PASS**. A change to those command exit semantics is proposed separately and requires the appropriate compatibility/governance approval.
+
 When running directly from a source checkout rather than an installed release asset, substitute `node /path/to/Ascout/dist/cli.js` for `ascout` in the examples below.
 
 ### Package identity and future installation
diff --git a/THIRD_PARTY_NOTICES.md b/THIRD_PARTY_NOTICES.md
index b357849..f87e9f9 100644
--- a/THIRD_PARTY_NOTICES.md
+++ b/THIRD_PARTY_NOTICES.md
@@ -1,11 +1,18 @@
 # Third-Party Notices
 
-**Status:** T086 exact-version dependency license/provenance review  
+**Status:** Current direct-dependency reconciliation (2026-10-08), preserving historical T086 evidence  
 **Scope:** direct dependencies intentionally selected for Ascout M1, bound to the current committed manifest and lockfile.
 
 This file records the exact direct third-party packages selected by Ascout and the evidence used to bind those selections to the committed lockfile. Exact transitive versions, registry locations, integrity digests, and license metadata are recorded in `package-lock.json` where npm provides those fields.
 
-## Current candidate binding
+## Current manifest/lockfile reconciliation (2026-10-08)
+
+- Runtime direct dependencies: **2** — `cross-spawn@7.0.6` (MIT) and `playwright@1.63.0` (Apache-2.0).
+- Direct development dependencies: **6** — `@types/node`, `@vitest/coverage-v8`, `jest`, `typescript`, `vite`, `vitest` at the versions listed below.
+- The current eight direct dependencies are represented in the notice ledger below. `playwright-core@1.63.0` is a transitive package, not a third direct runtime dependency.
+- The exact current npm graph and integrity records are committed in `package-lock.json`. This reconciliation does not imply a new npm release, a security audit, or any change to historical T086 evidence.
+
+## Historical T086 candidate binding (2026-08; preserved)
 
 T086 revalidated this ledger against canonical `main` at `a9bae09a71b4ff92097182a8d97f5ff6a0511603`.
 
@@ -50,7 +57,7 @@ Security/audit results are evidence for the specific resolved graph at the cited
 
 ## T086 license/provenance reconciliation
 
-All seven direct packages declared by the current candidate are represented below at their exact locked versions. The current direct set contains Apache-2.0 and MIT licenses only. No direct copyleft, source-available, non-commercial, field-of-use, database, or data-license restriction was identified in the manifest/lockfile evidence reviewed for T086.
+The historical T086 candidate contained seven direct packages at its then-locked versions. The current manifest contains eight direct packages, all listed below including Playwright 1.63.0. The current direct set contains Apache-2.0 and MIT licenses only. No direct copyleft, source-available, non-commercial, field-of-use, database, or data-license restriction was identified in the manifest/lockfile evidence reviewed for T086.
 
 This conclusion is scoped to the exact direct package versions below. Transitive packages remain separately represented by the committed lockfile and may use other permissive SPDX licenses. A future dependency/version change requires a fresh provenance/license reconciliation before release claims are updated.
 
@@ -64,6 +71,16 @@ This conclusion is scoped to the exact direct package versions below. Transitive
 - Registry tarball: `https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz`
 - SRI: `sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==`
 
+### `playwright` 1.63.0
+
+- Role: product runtime dependency for qualified browser-testing capabilities.
+- License: Apache-2.0
+- Upstream: `microsoft/playwright`, tag `v1.63.0`
+- Registry tarball: `https://registry.npmjs.org/playwright/-/playwright-1.63.0.tgz`
+- SRI: `sha512-+7ziBLidS4NaNCdt57SUDT+wYmmd5fmiQejUic/kb+YsYSCPyOOE9sebzMjNmQrsnNpDJqd4WHvV/8lfKfUDUg==`
+- Transitive package: `playwright-core@1.63.0` (Apache-2.0), registry tarball `https://registry.npmjs.org/playwright-core/-/playwright-core-1.63.0.tgz`, SRI `sha512-rYCsBF/M5HjUch52bbtVONEFjv6Xu8sm8h72dNlR5bzIE1fvC/bxgspzkjSfU+MweEMmPM8KJebG6nnyxo5mCg==`
+- This notice records package rights and lockfile binding; it does not assert that browser binaries are included in Ascout's distributable package.
+
 ### `@types/node` 22.20.1
 
 - Role: development-only Node.js type declarations aligned to the Node 22 support floor
diff --git a/tests/third-party-notices.test.ts b/tests/third-party-notices.test.ts
new file mode 100644
index 0000000..1e8519e
--- /dev/null
+++ b/tests/third-party-notices.test.ts
@@ -0,0 +1,39 @@
+import { readFileSync } from "node:fs";
+import { describe, expect, it } from "vitest";
+
+const manifest = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")) as {
+  dependencies: Record<string, string>;
+  devDependencies: Record<string, string>;
+};
+const lock = JSON.parse(readFileSync(new URL("../package-lock.json", import.meta.url), "utf8")) as {
+  packages: Record<string, { version?: string; license?: string; resolved?: string; integrity?: string }>;
+};
+const notices = readFileSync(new URL("../THIRD_PARTY_NOTICES.md", import.meta.url), "utf8");
+const declared = Object.entries({ ...manifest.dependencies, ...manifest.devDependencies });
+
+describe("direct dependency notice integrity", () => {
+  it("requires a nonempty direct-dependency set to prevent vacuous success", () => {
+    expect(declared.length).toBeGreaterThan(0);
+  });
+
+  for (const [name, version] of declared) {
+    it(`contains exact provenance for ${name}@${version}`, () => {
+      const locked = lock.packages[`node_modules/${name}`];
+      expect(locked).toBeDefined();
+      expect(locked?.version).toBe(version);
+
+      const heading = `### \`${name}\` ${version}`;
+      const start = notices.indexOf(heading);
+      expect(start).toBeGreaterThanOrEqual(0);
+
+      const next = notices.indexOf("\n### ", start + heading.length);
+      const section = notices.slice(start, next < 0 ? undefined : next);
+      expect(locked?.license).toBeTruthy();
+      expect(locked?.resolved).toBeTruthy();
+      expect(locked?.integrity).toBeTruthy();
+      expect(section).toContain(`License: ${locked?.license}`);
+      expect(section).toContain(locked?.resolved);
+      expect(section).toContain(locked?.integrity);
+    });
+  }
+});
```

## Full file at head: README.md
```
    1| # Ascout
    2| 
    3| > **Verify everything AI ships.**  
    4| > **Know exactly what passed, failed, and was never checked.**
    5| 
    6| Ascout is a local, evidence-bound verification layer for AI-built software. It inspects the exact Git working-tree state, discovers supported project-local verification tools, runs bounded checks, and emits a receipt that distinguishes what was proved from what failed, was refused, remained unresolved, or was not run.
    7| 
    8| Ascout's M1 goal is deliberately narrow: make changed-code verification harder to overclaim without turning the tool into a CI platform, cloud service, agent framework, or untrusted-code sandbox.
    9| 
   10| ## Status
   11| 
   12| Ascout has completed canonical **M1 release hardening** and the bounded **M2 selection-configuration fidelity** milestone. M2 adds benchmark-backed single-package nested Jest/Vitest configuration fidelity while preserving the M1 receipt, trust, admission, dependency, and publication boundaries. The package is version `0.1.0`, remains `private: true`, and is not published to npm. Spec 013 qualifies an npm-compatible tarball for GitHub Release distribution; a GitHub Release is separate from npm-registry publication.
   13| 
   14| Canonical T087 selected the repository package identity `@thehalfmoon/ascout` while preserving the executable name `ascout`. The scoped identity is a repository decision, not a claim that authenticated npm scope ownership or publication authority has been proven; any future publication requires separate authenticated npm scope/ownership evidence and separate release/publication authority.
   15| 
   16| GitHub `main`, the canonical Spec Kit artifacts under `specs/001-changed-code-verification-receipt/` and `specs/002-selection-config-fidelity/`, and merged task PRs are the source of current implementation truth. The simplified M1 builder map remains in `specs/001-changed-code-verification-receipt/IMPLEMENTATION_RUNBOOK.md`.
   17| 
   18| ## What M1 does
   19| 
   20| For a supported trusted local repository, `ascout check` can:
   21| 
   22| - bind verification to a privacy-safe repository identity and the exact full Git source-start object ID;
   23| - compare the working tree against that exact source-start HEAD rather than a guessed or later-resolved base;
   24| - include tracked and nonignored untracked source state in a deterministic tree digest while excluding Ascout's own `.ascout/` runtime area;
   25| - discover fixed semantic tasks for TypeScript, ESLint, Vitest, Jest, and basic pytest workflows when the required local tools/configuration are present;
   26| - execute project-local commands without constructing an arbitrary shell command string;
   27| - bound command runtime, captured output, widening, flake observations, run retention, and agent-receipt size;
   28| - refuse changed effective command/configuration surfaces by default until the human caller explicitly admits that surface for one invocation;
   29| - record task `PASS`/`FAIL`/`FLAKY`/`BLOCKED`/`ERROR`/`NOT_APPLICABLE`/`NOT_RUN` distinctions instead of collapsing omissions into green;
   30| - use native related-test selection where supported, with at most one bounded widening pass when evidence requires it;
   31| - normalize LCOV line evidence and report changed executable lines as `EXERCISED`, `NOT_EXERCISED`, or `UNRESOLVED`;
   32| - detect source drift between the beginning and end of a check;
   33| - perform bounded exact failing-test reruns to distinguish reproduced failure, contradictory/flaky observations, and unknown reproduction;
   34| - emit terminal, JSON, or bounded agent receipts from one semantically validated truth model;
   35| - persist evidence under `.ascout/` with bounded completed-run retention and documented redaction/truncation facts.
   36| 
   37| ## What M2 adds
   38| 
   39| M2 is deliberately narrower than the broader post-M1 research roadmap. For a supported **single-package** JavaScript/TypeScript repository, when no existing root-level Jest/Vitest configuration is effective, Ascout may use exactly one recognized nested Jest or Vitest config as the runner's explicit `--config` authority. Root configuration keeps precedence, multiple nested candidates fail closed, and a changed selected nested config still requires explicit per-invocation changed-command-surface admission.
   40| 
   41| The founding `react-hook-form-value-as-date@2` selector miss was replayed after the repair: the frozen oracle test became an Ascout selector hit, historical T078 publication remained unchanged, and unavailable benchmark evidence remained unavailable. M2 did not add arbitrary package-script execution, generic command reconstruction, dependency/import graphs, basic-workspace nested-config ownership, a new runtime dependency, a receipt version, persistent trust, npm publication, a GitHub Release, or a release tag.
   42| 
   43| ## What M1/M2 do not claim
   44| 
   45| Ascout M1/M2 do **not** claim to be:
   46| 
   47| - an untrusted-repository sandbox or malware containment system;
   48| - a child-process network isolation layer;
   49| - a dependency installer or environment provisioner;
   50| - a CI/CD service, remote execution service, or SARIF platform;
   51| - a generic workflow engine or plugin SDK;
   52| - a database-backed test intelligence service;
   53| - a semantic code graph, model-powered reviewer, or autonomous fixing agent;
   54| - proof that a passing selected test set means every possible regression has been excluded;
   55| - proof of causality that a failure was introduced by the current change when comparative evidence is absent;
   56| - universal secret detection;
   57| - a published stable npm package yet.
   58| 
   59| A stable receipt is evidence of the observations Ascout actually made. It is not permission to infer evidence that was never collected.
   60| 
   61| ## Trust model
   62| 
   63| Ascout v0.x is intended for the developer's own **trusted local Git repository**. Repository commands, package scripts, compilers, linters, test runners, and configuration loaded by those tools execute with the developer's local process authority. They may read or modify files, start processes, access credentials available to the process, or use the network according to their own environment.
   64| 
   65| Ascout does not silently install repository dependencies and does not make an otherwise untrusted repository safe to execute. See [`SECURITY.md`](SECURITY.md) for the security/reporting boundary.
   66| 
   67| ## Requirements
   68| 
   69| For the current source build:
   70| 
   71| - Node.js **22 or newer**;
   72| - Git;
   73| - npm for the committed lockfile workflow;
   74| - project-local verification tools required by the tasks you expect Ascout to run.
   75| 
   76| Project CI runs Node 22 and Node 24 on Linux, macOS, and Windows Server 2025. Supported-platform evidence is kept explicit: platform-specific test debt is not converted into a false green result.
   77| 
   78| ## Use from the repository today
   79| 
   80| The canonical package identity is selected, the package remains `private: true`, and Ascout is not published to npm. Use an exact source checkout, or an exact verified GitHub Release tarball asset when one is available; GitHub Release distribution does not imply npm-registry publication.
   81| 
   82| ```sh
   83| git clone https://github.com/TheHalfMoon/Ascout.git
   84| cd Ascout
   85| npm ci --ignore-scripts --no-audit --no-fund
   86| npm run build
   87| node dist/cli.js
   88| ```
   89| 
   90| The last command prints usage and exits with a usage error because a command is required. The CLI surface is:
   91| 
   92| ```text
   93| ascout init
   94| ascout doctor
   95| ascout check [--allow-changed-command-surface] [--format json|agent]
   96| ascout review [--format json|terminal]
   97| ascout test [--profile quick|standard|deep|release] [--format json|terminal]
   98| ```
   99| 
  100| **Current command semantics (v0.1.0):** `ascout check` executes supported local verification tasks and produces an evidence receipt. `ascout review` presently reports review scope or unavailable review execution; it does **not** run a code-review engine. `ascout test` presently creates a test plan; it does **not** execute that plan. Both `review` and `test` can currently exit with code 0 even though no review or advanced test execution took place. That exit status is **not an assurance PASS**. A change to those command exit semantics is proposed separately and requires the appropriate compatibility/governance approval.
  101| 
  102| When running directly from a source checkout rather than an installed release asset, substitute `node /path/to/Ascout/dist/cli.js` for `ascout` in the examples below.
  103| 
  104| ### Package identity and future installation
  105| 
  106| The canonical repository package identity is:
  107| 
  108| ```text
  109| @thehalfmoon/ascout
  110| ```
  111| 
  112| The executable name remains:
  113| 
  114| ```text
  115| ascout
  116| ```
  117| 
  118| This identity selection does not prove authenticated ownership of the npm scope and does not mean the package has been published. Do not run a registry install based only on this repository decision. If a future task separately proves npm scope ownership, authorizes publication, and publishes the package, the expected global-install shape is:
  119| 
  120| ```sh
  121| npm install --global @thehalfmoon/ascout
  122| ```
  123| 
  124| Until separate npm publication evidence exists, do not use an npm-registry install. Use the source-checkout workflow above, or an exact verified GitHub Release tarball asset when one is available.
  125| 
  126| ## Quickstart in a trusted project
  127| 
  128| Run the built Ascout executable from the root of the Git repository you want to verify.
  129| 
  130| ### 1. Initialize minimal local configuration
  131| 
  132| ```sh
  133| ascout init
  134| ```
  135| 
  136| `init` creates `ascout.config.json` with version 1 when it is absent and ensures `.ascout/` appears in `.gitignore`. It does not install dependencies, create hooks, or grant command-surface admission.
  137| 
  138| ### 2. Inspect discovery without running verification tasks
  139| 
  140| ```sh
  141| ascout doctor
  142| ```
  143| 
  144| `doctor` reports privacy-safe repository identity, project/tool discovery, configuration source, effective command-authority counts, and changed-file facts. It does not execute the verification task matrix.
  145| 
  146| ### 3. Run verification
  147| 
  148| ```sh
  149| ascout check
  150| ```
  151| 
  152| The default terminal receipt tells you what ran, what passed or failed, what Ascout refused or could not prove, changed-code exercise state, source stability, completeness, and the resulting exit code.
  153| 
  154| For machine-readable output:
  155| 
  156| ```sh
  157| ascout check --format json
  158| ```
  159| 
  160| For a bounded agent-oriented receipt:
  161| 
  162| ```sh
  163| ascout check --format agent
  164| ```
  165| 
  166| All formats derive from the same semantically validated receipt model.
  167| 
  168| ## Changed-command admission
  169| 
  170| A changed command surface is an effective repository file that influences a command Ascout would execute or configuration a supported tool would load. Examples can include package scripts, `ascout.config.json`, TypeScript/ESLint/Vitest/Jest configuration, and the effective basic-pytest configuration.
  171| 
  172| If such a surface is part of the current source change, ordinary `ascout check` refuses the affected task before launch and records:
  173| 
  174| ```text
  175| NOT_RUN(command_surface_changed)
  176| ```
  177| 
  178| That refusal is intentional. Review the changed command/configuration surface yourself. If you decide it is safe for this invocation, run:
  179| 
  180| ```sh
  181| ascout check --allow-changed-command-surface
  182| ```
  183| 
  184| Important properties of this admission:
  185| 
  186| - it is explicit and human-supplied;
  187| - it applies only to that invocation;
  188| - it is recorded in the receipt with the affected paths;
  189| - it is not persisted as a trust grant;
  190| - the next ordinary invocation refuses again when the changed surface is still relevant;
  191| - agent instructions, hooks, and automation must not inject the flag automatically.
  192| 
  193| The override admits execution of the reviewed changed surface; it does not turn the repository into sandboxed or trusted-by-Ascout code.
  194| 
  195| ## Fixed verification tasks
  196| 
  197| M1 has four fixed semantic task keys:
  198| 
  199| | Task | Purpose | Typical local authority |
  200| | --- | --- | --- |
  201| | `typecheck` | TypeScript type checking | explicit Ascout override, package script, or unambiguous project-local `tsc` |
  202| | `lint` | ESLint verification | explicit override, package script, or supported project-local ESLint/configuration |
  203| | `test` | JavaScript/TypeScript tests and changed-code exercise evidence | supported project-local Vitest or Jest workflow |
  204| | `pytestBasic` | basic pytest execution | supported project-local pytest invocation/configuration |
  205| 
  206| Discovery is fail-closed when the project/tool/configuration state is ambiguous or unavailable. M1 does not invent a command, install a missing tool, or silently reinterpret an unsupported workflow as verified.
  207| 
  208| `ascout.config.json` can configure the fixed task surface, but M1 does not support arbitrary task keys, generic prerequisite graphs, or a persistent admission setting.
  209| 
  210| ## Changed-code exercise evidence
  211| 
  212| Passing tests are not the same as proving that changed executable lines were exercised. For supported JavaScript test paths, Ascout binds final LCOV evidence to changed new-line ranges and reports each material changed executable line as:
  213| 
  214| - `EXERCISED` — the final valid coverage evidence observed execution;
  215| - `NOT_EXERCISED` — the line is executable and final valid evidence observed zero execution;
  216| - `UNRESOLVED` — Ascout cannot make a valid exercise claim and records why.
  217| 
  218| If a narrowed related-test pass leaves insufficient evidence, Ascout may run at most one bounded wider pass. It does not recursively widen until green. A stable run with a remaining material exercise gap does not become exit 0 merely because selected tests passed.
  219| 
  220| ## Source and evidence binding
  221| 
  222| A receipt is bound to the source Ascout actually observed:
  223| 
  224| - `source.start.head_sha` is the exact full Git object ID resolved at source start;
  225| - for `working_tree_vs_head`, `comparison.base_ref` must equal that same exact object ID;
  226| - SHA-1 repositories use 40-hex object IDs and SHA-256 repositories use 64-hex object IDs;
  227| - source state is rehashed at the end so drift is reported independently from task completeness;
  228| - persisted paths are canonical repository/run-relative slash-separated paths;
  229| - invalid raw absolute, drive, UNC, URI, backslash, traversal, duplicate-separator, or trailing-separator spellings are rejected before lossy normalization can repair them into valid-looking evidence;
  230| - evidence/artifact references must resolve inside the run/task contract.
  231| 
  232| The repository identity itself is privacy-safe: Ascout persists a hashed normalized remote identity when available or a hashed canonical-local identity, rather than persisting raw credential-bearing origins or raw absolute local repository paths.
  233| 
  234| ## Receipts and local artifacts
  235| 
  236| Runtime evidence lives under:
  237| 
  238| ```text
  239| .ascout/
  240| ```
  241| 
  242| The directory is ignored by default. Completed-run retention is bounded (20 by default), and an active run is not removed to satisfy retention.
  243| 
  244| Evidence can contain repository/tool output and should be treated as potentially sensitive. Ascout applies its documented redaction boundary for recognized and configured secret-bearing environment values and records truncation/redaction facts, but redaction is best-effort rather than universal secret discovery.
  245| 
  246| Do not commit `.ascout/` runtime evidence or put unnecessary real secrets/private customer data into reproductions.
  247| 
  248| ## Exit semantics
  249| 
  250| Ascout uses exit status as part of the evidence contract. The important rule is that stronger failures are not hidden behind a success status, and a materially incomplete stable run cannot report green by omission.
  251| 
  252| At a high level:
  253| 
  254| - `0` means the semantically validated run reached the repository's success conditions;
  255| - source drift has higher precedence than a remaining exercise gap;
  256| - a remaining material `NOT_EXERCISED` or `UNRESOLVED` changed-code gap maps to the dedicated incomplete/gap exit rather than 0;
  257| - internal/control validity failures remain distinct from ordinary repository-command failure;
  258| - refused or unrun required work remains visible in receipt completeness/status rather than being counted as passed.
  259| 
  260| Consumers should use the receipt fields together with the exit status instead of reducing the receipt to a single boolean.
  261| 
  262| ## Package boundary
  263| 
  264| T082 added a positive npm `files` allowlist and a real package-content gate. The current release surface is limited to the built `dist` tree plus npm-mandated metadata; tests, source, specs, benchmarks, `.ascout/`, fixtures, logs, secrets, and coverage output are not intended package contents.
  265| 
  266| T087 selected `@thehalfmoon/ascout` as the canonical repository package identity while preserving `bin.ascout = "./dist/cli.js"`. That packaging and identity proof does **not** mean a package has been published: `package.json` remains `private: true`, and future publication still requires separate authenticated npm scope/ownership evidence and separate publication authority.
  267| 
  268| ## Benchmarks
  269| 
  270| The founding benchmark under [`benchmarks/`](benchmarks/) is evidence for selector behavior, changed-code gap behavior, drift/determinism/flake semantics, and integrity assertions. It preserves unavailable comparator evidence as unavailable and publishes selector misses rather than hiding them behind an aggregate.
  271| 
  272| It is not a claim that Ascout has perfect recall or that historical corpus performance predicts every repository. See [`benchmarks/README.md`](benchmarks/README.md) and [`benchmarks/manifest.json`](benchmarks/manifest.json) for the frozen corpus, acquisition/licensing rules, and exact evidence identities.
  273| 
  274| ## Project verification
  275| 
  276| From an Ascout source checkout:
  277| 
  278| ```sh
  279| npm ci --ignore-scripts --no-audit --no-fund
  280| npm run typecheck
  281| npm test
  282| npm run build
  283| ```
  284| 
  285| Project CI runs this matrix on Linux, macOS, and Windows with Node 22 and Node 24. Release hardening records supported-platform debt explicitly instead of skipping or suppressing it.
  286| 
  287| T088 performs the final clean-checkout M1 release-candidate rehearsal across the canonical quickstart, contract/semantic/integration gates, package inspection, benchmark evidence, and supported-platform proof. T092 performs the bounded M2 selection-config-fidelity closeout against the same six-lane platform matrix and Spec 002 benchmark evidence. Neither task publishes npm or creates a GitHub Release/tag.
  288| 
  289| ## Contributing and security
  290| 
  291| Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing material changes. Ascout uses a constitution/Spec Kit/Ponytail workflow, one canonical task per task-scoped branch/PR, forward-only review repairs, exact-head evidence, and provenance review for third-party material.
  292| 
  293| For vulnerabilities and the trusted-local execution boundary, see [`SECURITY.md`](SECURITY.md). Do not disclose an undisclosed vulnerability in a public issue or pull request.
  294| 
  295| ## License and provenance
  296| 
  297| Ascout is licensed under Apache-2.0. See [`LICENSE`](LICENSE).
  298| 
  299| Third-party dependency/code provenance is tracked in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`docs/legal/CODE_PROVENANCE.md`](docs/legal/CODE_PROVENANCE.md). T086 reconciled those records against the exact release-hardening dependency graph; the canonical lockfile remains the machine-readable transitive dependency source for the current candidate.
  300| 
  301| The founding specification workflow is pinned in [`.specify/PROVENANCE.md`](.specify/PROVENANCE.md).
  302| 
  303| ## Strategic research
  304| 
  305| The 2026-08-26 major product/testing review and post-M1 roadmap are preserved under [`docs/strategy/`](docs/strategy/README.md). These documents are **non-authoritative research/planning inputs**. They do not reorder or expand the current canonical Spec Kit authority chain, and future capabilities require separate canonicalization and authorization before implementation.
```

## Full file at head: THIRD_PARTY_NOTICES.md
```
    1| # Third-Party Notices
    2| 
    3| **Status:** Current direct-dependency reconciliation (2026-10-08), preserving historical T086 evidence  
    4| **Scope:** direct dependencies intentionally selected for Ascout M1, bound to the current committed manifest and lockfile.
    5| 
    6| This file records the exact direct third-party packages selected by Ascout and the evidence used to bind those selections to the committed lockfile. Exact transitive versions, registry locations, integrity digests, and license metadata are recorded in `package-lock.json` where npm provides those fields.
    7| 
    8| ## Current manifest/lockfile reconciliation (2026-10-08)
    9| 
   10| - Runtime direct dependencies: **2** — `cross-spawn@7.0.6` (MIT) and `playwright@1.63.0` (Apache-2.0).
   11| - Direct development dependencies: **6** — `@types/node`, `@vitest/coverage-v8`, `jest`, `typescript`, `vite`, `vitest` at the versions listed below.
   12| - The current eight direct dependencies are represented in the notice ledger below. `playwright-core@1.63.0` is a transitive package, not a third direct runtime dependency.
   13| - The exact current npm graph and integrity records are committed in `package-lock.json`. This reconciliation does not imply a new npm release, a security audit, or any change to historical T086 evidence.
   14| 
   15| ## Historical T086 candidate binding (2026-08; preserved)
   16| 
   17| T086 revalidated this ledger against canonical `main` at `a9bae09a71b4ff92097182a8d97f5ff6a0511603`.
   18| 
   19| - `package.json` blob: `e5d99fcd1bb87fa3adec2629d949bde933000bf7`
   20| - `package-lock.json` blob: `e51f0bddb953235c1a391718eabfab5a6c680832`
   21| - Product runtime dependency count: 1 (`cross-spawn@7.0.6`)
   22| - Direct development dependency count: 6 (`@types/node`, `@vitest/coverage-v8`, `jest`, `typescript`, `vite`, `vitest`)
   23| - Direct manifest/lockfile reconciliation: complete; no direct dependency is omitted from this notice ledger.
   24| 
   25| The committed npm lockfile is the canonical machine-readable graph for this candidate. The T086 review does not upgrade dependencies, regenerate the lockfile, alter package identity, publish to npm, or claim that a point-in-time security audit is permanent.
   26| 
   27| ## Lock generation evidence
   28| 
   29| - Evidence branch: `evidence/t003-lockgen-2026-08-22` (the date component is the Asia/Riyadh local date; the corresponding GitHub Actions timestamps are on 2026-08-21 UTC).
   30| - Evidence commit containing the generated lockfile: `81e2850e06a097abed5a7566aded39fceb330800`
   31| - Original generated `package-lock.json` blob: `751fdf89c10d26a1875844626ad6c336b28d051b`
   32| - GitHub Actions generation run: `32535056565`
   33| - Runner OS: Ubuntu 24.04
   34| - Node: `22.0.0`
   35| - npm resolver: `10.9.4`
   36| - Generation command: `npm install --package-lock-only --ignore-scripts --audit=false --fund=false`
   37| - Reproduction check: `npm ci --ignore-scripts --audit=false --fund=false` — PASS
   38| - Exact direct-resolution check — PASS
   39| - `npm ls --all` — exited successfully; its tree truthfully reports platform-, peer-, and engine-inapplicable optional dependencies as `UNMET OPTIONAL DEPENDENCY` rather than treating them as required install failures.
   40| - Tool execution on Node 22.0.0: TypeScript `6.0.3`, Vite `6.4.3`, Vitest `4.1.10` — PASS
   41| - Generation-time security check: `npm audit --package-lock-only --audit-level=high` reported `found 0 vulnerabilities`.
   42| 
   43| ### Node 22.0.0 engine-strict verification
   44| 
   45| A follow-up evidence run `32535678363` used the same package manifest and unchanged lockfile blob on Node `22.0.0` with npm `10.9.4` and added an engine-strict installation gate:
   46| 
   47| - `npm ci --engine-strict --ignore-scripts --audit=false --fund=false` — PASS
   48| - `@napi-rs/lzma-linux-x64-gnu@1.5.1`, an optional dependency of `rollup@4.62.5` whose own engine range starts at Node 22.20, was omitted by npm on Node 22.0.0 as an inapplicable optional dependency.
   49| - The workflow asserted that this optional package was absent after the engine-strict install.
   50| - Vite `6.4.3` executed on Node `22.0.0` after that install — PASS.
   51| - Vitest `4.1.10` executed on Node `22.0.0` after that install — PASS.
   52| - The follow-up audit again reported `found 0 vulnerabilities` for the resolved lockfile graph.
   53| 
   54| The stricter engine range of an omitted optional package therefore does not redefine Ascout's Node `>=22` support floor. The evidence above is deliberately scoped to the tested Ubuntu x64 environment and does not claim an untested platform result.
   55| 
   56| Security/audit results are evidence for the specific resolved graph at the cited runs; they are not permanent security claims.
   57| 
   58| ## T086 license/provenance reconciliation
   59| 
   60| The historical T086 candidate contained seven direct packages at its then-locked versions. The current manifest contains eight direct packages, all listed below including Playwright 1.63.0. The current direct set contains Apache-2.0 and MIT licenses only. No direct copyleft, source-available, non-commercial, field-of-use, database, or data-license restriction was identified in the manifest/lockfile evidence reviewed for T086.
   61| 
   62| This conclusion is scoped to the exact direct package versions below. Transitive packages remain separately represented by the committed lockfile and may use other permissive SPDX licenses. A future dependency/version change requires a fresh provenance/license reconciliation before release claims are updated.
   63| 
   64| ## Direct dependencies
   65| 
   66| ### `cross-spawn` 7.0.6
   67| 
   68| - Role: product runtime dependency
   69| - License: MIT
   70| - Upstream: `moxystudio/node-cross-spawn`, tag `v7.0.6`
   71| - Registry tarball: `https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz`
   72| - SRI: `sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==`
   73| 
   74| ### `playwright` 1.63.0
   75| 
   76| - Role: product runtime dependency for qualified browser-testing capabilities.
   77| - License: Apache-2.0
   78| - Upstream: `microsoft/playwright`, tag `v1.63.0`
   79| - Registry tarball: `https://registry.npmjs.org/playwright/-/playwright-1.63.0.tgz`
   80| - SRI: `sha512-+7ziBLidS4NaNCdt57SUDT+wYmmd5fmiQejUic/kb+YsYSCPyOOE9sebzMjNmQrsnNpDJqd4WHvV/8lfKfUDUg==`
   81| - Transitive package: `playwright-core@1.63.0` (Apache-2.0), registry tarball `https://registry.npmjs.org/playwright-core/-/playwright-core-1.63.0.tgz`, SRI `sha512-rYCsBF/M5HjUch52bbtVONEFjv6Xu8sm8h72dNlR5bzIE1fvC/bxgspzkjSfU+MweEMmPM8KJebG6nnyxo5mCg==`
   82| - This notice records package rights and lockfile binding; it does not assert that browser binaries are included in Ascout's distributable package.
   83| 
   84| ### `@types/node` 22.20.1
   85| 
   86| - Role: development-only Node.js type declarations aligned to the Node 22 support floor
   87| - License: MIT
   88| - Upstream: `DefinitelyTyped/DefinitelyTyped`, package path `types/node`
   89| - Registry tarball: `https://registry.npmjs.org/@types/node/-/node-22.20.1.tgz`
   90| - SRI: `sha512-EANqOCF9QFyra+4pfxUcX9STKJpCLjMbObVzljIJomAWSnuSIEAvyzEU53GaajbXJEgdh0iEcPL+DGvpUd4k1Q==`
   91| 
   92| ### `@vitest/coverage-v8` 4.1.11
   93| 
   94| - Role: development-only V8 coverage provider used by the Vitest integration and changed-code exercise tests
   95| - License: MIT
   96| - Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/coverage-v8`
   97| - Registry tarball: `https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.11.tgz`
   98| - SRI: `sha512-8MVGEFnJIcdGjcbfKmeq8z0pZHH0JlVtoVZH9Q/qwUp6wyFnEJUBMrw9DCaj+ra3vShGmhavjalMIhPNxZAUcw==`
   99| 
  100| ### `jest` 30.4.2
  101| 
  102| - Role: development-only Jest runner used to qualify Ascout's supported Jest integration
  103| - License: MIT
  104| - Upstream: `jestjs/jest`, tag `v30.4.2`
  105| - Registry tarball: `https://registry.npmjs.org/jest/-/jest-30.4.2.tgz`
  106| - SRI: `sha512-Yi1jqNC/Oq0N4hBgNH/YvBpP1P57QqundgytzYqy3yqAa7NZPNjSoi4SGbRAXDMdBzNE6xBCi5U7RgfrvMEUVQ==`
  107| 
  108| ### `typescript` 6.0.3
  109| 
  110| - Role: development-only compiler/typechecker
  111| - License: Apache-2.0
  112| - Upstream: `microsoft/TypeScript`, tag `v6.0.3`
  113| - Registry tarball: `https://registry.npmjs.org/typescript/-/typescript-6.0.3.tgz`
  114| - SRI: `sha512-y2TvuxSZPDyQakkFRPZHKFm+KKVqIisdg9/CZwm9ftvKXLP8NRWj38/ODjNbr43SsoXqNuAisEf1GdCxqWcdBw==`
  115| 
  116| ### `vite` 6.4.3
  117| 
  118| - Role: development-only peer/runtime substrate selected for Vitest while preserving the Ascout Node `>=22` floor
  119| - License: MIT
  120| - Upstream: `vitejs/vite`, tag `v6.4.3`, package path `packages/vite`
  121| - Registry tarball: `https://registry.npmjs.org/vite/-/vite-6.4.3.tgz`
  122| - SRI: `sha512-NTKlcQjlAK7MlQoyb6LgaqHc8sso/pVyUJYWMws3jg21uTJw/LddqIFPcPqP6PzpgbIcZyKI85sFE4HBrQDA8A==`
  123| 
  124| ### `vitest` 4.1.11
  125| 
  126| - Role: development-only test runner
  127| - License: MIT
  128| - Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/vitest`
  129| - Registry tarball: `https://registry.npmjs.org/vitest/-/vitest-4.1.11.tgz`
  130| - SRI: `sha512-fhACrNXUidIbGSBr5FlbuBkO7VWC1ZyLl0DO4CU2DrQoAPxX84Ysxs+HeGQpii5lZWV1Q4gBZTTu49mF+A6Edw==`
  131| 
  132| ## Transitive dependencies
  133| 
  134| `package-lock.json` is the canonical machine-readable record for the exact resolved transitive graph used by this revision, including registry `resolved` URLs, SRI `integrity` values, and license metadata where npm records it. Optional entries can legitimately remain recorded even when npm omits them on a particular platform or Node version.
  135| 
  136| The T086 review does not treat process isolation, development-only status, or npm registry availability as a substitute for license terms. It also does not assume that a permissive direct package makes every possible future bundled artifact attribution-free. The T082 package-content gate proves the current Ascout tarball surface separately; any future bundling/vendor change must re-evaluate redistribution and notice obligations.
  137| 
  138| This file does not replace any third-party license text or attribution that a future packaged distribution is legally required to carry.
  139| 
  140| ## Donor snapshot — google/artemis (ARTEMIS A0)
  141| 
  142| - Upstream: `https://github.com/google/artemis`
  143| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  144| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  145| - License: Apache-2.0
  146| - Ascout paths: `vendor/google-artemis/**` plus separately reviewed adapters
  147| - Use type: copied + adapted, Class C provenance
  148| - Snapshot content: complete repository snapshot at the exact commit (796 blob paths)
  149| - Notice preservation: donor LICENSE, copyright headers, and notice material preserved inside the immutable snapshot; no modifications inside the snapshot
  150| - Runtime authority: none granted by source presence; activation requires separate phased authorization and qualification
  151| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
  152| 
  153| ## Donor snapshot — google/artemis (ARTEMIS A13 release admission)
  154| 
  155| - Upstream: `https://github.com/google/artemis`
  156| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  157| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  158| - License: Apache-2.0
  159| - Release scope: contract, adapter, evidence, and documentation layers under `vendor/google-artemis/**`, `src/assurance/engines/mobile-artemis/**`, `python/ascout_mobile_bridge/**`, `schemas/mobile-artemis/**`, `docs/mobile/**`
  160| - Phases admitted: ARTEMIS-A0 through ARTEMIS-A12 closed canonically; A13 gates recorded in `docs/mobile/artemis-a13-release.md`
  161| - Donor telemetry: off by default; no telemetry destination admitted
  162| - Runtime authority: none granted by source presence or by release admission
  163| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
  164| ## Donor characterization — TheHalfMoon/Sentrdel (UA-P06)
  165| 
  166| - Upstream: `https://github.com/TheHalfMoon/Sentrdel` (same GitHub owner account as Ascout; this entry makes no statement about legal copyright ownership)
  167| - Pinned commit: `f5747319a50831ef7cee983d253c0ca5503c9a64` ("Merge PR #333: make Sentrdel developer-first and adoption-ready", 2026-09-16)
  168| - Pinned tree: `0d70de477fa403a416a8cff5576498e4c59a1689`
  169| - License: Apache-2.0 (root `LICENSE`, blob `45d3d38717ab6e5fd41a53a9b14184d0e93f1007`); no nested license file in the selected paths
  170| - Notice material: none at the pin (no `NOTICE` file; selected source files carry no copyright headers), so no notice text is carried
  171| - Use type: reference-only characterization (`SENTRDEL_INTEGRATION_MODES = ["REFERENCE_ONLY"]`). Ascout re-expresses observed rule identifiers, capability semantics, and path classifications in its own TypeScript; no Sentrdel source files are copied or vendored
  172| - Ascout paths: `src/assurance/security/sentrdel-*.ts` and their tests
  173| - Repository visibility: recorded as public at pin time; private as of 2026-10-10, so third parties may be unable to inspect the pinned source
  174| - Runtime authority: none; Sentrdel output enters only through the external-engine adapter boundary as observations, never as Ascout assurance
  175| - Provenance record: `src/assurance/security/sentrdel-source-pin.ts` (`provenance:sentrdel-pin-f5747319a50831ef7cee983d253c0ca5503c9a64`)
```

## Full file at head: tests/third-party-notices.test.ts
```
    1| import { readFileSync } from "node:fs";
    2| import { describe, expect, it } from "vitest";
    3| 
    4| const manifest = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")) as {
    5|   dependencies: Record<string, string>;
    6|   devDependencies: Record<string, string>;
    7| };
    8| const lock = JSON.parse(readFileSync(new URL("../package-lock.json", import.meta.url), "utf8")) as {
    9|   packages: Record<string, { version?: string; license?: string; resolved?: string; integrity?: string }>;
   10| };
   11| const notices = readFileSync(new URL("../THIRD_PARTY_NOTICES.md", import.meta.url), "utf8");
   12| const declared = Object.entries({ ...manifest.dependencies, ...manifest.devDependencies });
   13| 
   14| describe("direct dependency notice integrity", () => {
   15|   it("requires a nonempty direct-dependency set to prevent vacuous success", () => {
   16|     expect(declared.length).toBeGreaterThan(0);
   17|   });
   18| 
   19|   for (const [name, version] of declared) {
   20|     it(`contains exact provenance for ${name}@${version}`, () => {
   21|       const locked = lock.packages[`node_modules/${name}`];
   22|       expect(locked).toBeDefined();
   23|       expect(locked?.version).toBe(version);
   24| 
   25|       const heading = `### \`${name}\` ${version}`;
   26|       const start = notices.indexOf(heading);
   27|       expect(start).toBeGreaterThanOrEqual(0);
   28| 
   29|       const next = notices.indexOf("\n### ", start + heading.length);
   30|       const section = notices.slice(start, next < 0 ? undefined : next);
   31|       expect(locked?.license).toBeTruthy();
   32|       expect(locked?.resolved).toBeTruthy();
   33|       expect(locked?.integrity).toBeTruthy();
   34|       expect(section).toContain(`License: ${locked?.license}`);
   35|       expect(section).toContain(locked?.resolved);
   36|       expect(section).toContain(locked?.integrity);
   37|     });
   38|   }
   39| });
```
