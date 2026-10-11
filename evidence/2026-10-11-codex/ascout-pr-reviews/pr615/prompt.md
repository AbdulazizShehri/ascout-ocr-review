You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad..689c0b5ce0920e18d22be21f877d8767c0db1148
Pull request title (context only): test: use /dev/null for isolated Git config on every platform
Changed files: tests/cli.smoke.test.ts,tests/drift.contract.test.ts,tests/git-diff.test.ts,tests/git-tree-digest-bom.test.ts,tests/git-tree-digest.test.ts,tests/pr41-p0-regressions.contract.test.ts,tests/t081-cross-platform-receipt-golden.test.ts

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, and whether tests keep their assertion strength.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (0 reviewable / 7 total)

- mode: range
- from: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- to: 689c0b5ce0920e18d22be21f877d8767c0db1148
- merge_base: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- total_insertions: 7
- total_deletions: 7

~~- `tests/cli.smoke.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/drift.contract.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/git-diff.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/git-tree-digest-bom.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/git-tree-digest.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/pr41-p0-regressions.contract.test.ts` [modified] +1/-1 (excluded: default_path)~~
~~- `tests/t081-cross-platform-receipt-golden.test.ts` [modified] +1/-1 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- tests/cli.smoke.test.ts
- tests/drift.contract.test.ts
- tests/git-diff.test.ts
- tests/git-tree-digest-bom.test.ts
- tests/git-tree-digest.test.ts
- tests/pr41-p0-regressions.contract.test.ts
- tests/t081-cross-platform-receipt-golden.test.ts

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
diff --git a/tests/cli.smoke.test.ts b/tests/cli.smoke.test.ts
index 3c99391..e75c11b 100644
--- a/tests/cli.smoke.test.ts
+++ b/tests/cli.smoke.test.ts
@@ -18,7 +18,7 @@ const ENV_KEYS = [
 const originalCwd = process.cwd();
 const originalEnv = new Map(ENV_KEYS.map((key) => [key, process.env[key]]));
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/drift.contract.test.ts b/tests/drift.contract.test.ts
index c4fed79..2dc1d11 100644
--- a/tests/drift.contract.test.ts
+++ b/tests/drift.contract.test.ts
@@ -10,7 +10,7 @@ import { buildReceipt } from "../src/receipt/build.js";
 import { validateReceiptSemantics, type SourceStateV1 } from "../src/receipt/model.js";
 
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_TEST_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/git-diff.test.ts b/tests/git-diff.test.ts
index a9810be..61fc5f6 100644
--- a/tests/git-diff.test.ts
+++ b/tests/git-diff.test.ts
@@ -17,7 +17,7 @@ import {
 } from "../src/git.js";
 
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/git-tree-digest-bom.test.ts b/tests/git-tree-digest-bom.test.ts
index cec7377..0b2a300 100644
--- a/tests/git-tree-digest-bom.test.ts
+++ b/tests/git-tree-digest-bom.test.ts
@@ -6,7 +6,7 @@ import { afterEach, describe, expect, it } from "vitest";
 import { readTreeDigestV1 } from "../src/git.js";
 
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/git-tree-digest.test.ts b/tests/git-tree-digest.test.ts
index a3d7b48..97b4867 100644
--- a/tests/git-tree-digest.test.ts
+++ b/tests/git-tree-digest.test.ts
@@ -28,7 +28,7 @@ const BASE_INDEX = [
   { path: "tests/__snapshots__/ui.snap", mode: "100644", oid: "2".repeat(40), stage: 0 },
 ] as const;
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_TEST_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/pr41-p0-regressions.contract.test.ts b/tests/pr41-p0-regressions.contract.test.ts
index 93b27c1..497af17 100644
--- a/tests/pr41-p0-regressions.contract.test.ts
+++ b/tests/pr41-p0-regressions.contract.test.ts
@@ -17,7 +17,7 @@ const originalEnv = new Map([
   ["ASCOUT_PR41_SECRET", process.env.ASCOUT_PR41_SECRET],
   ["GITHUB_TOKEN", process.env.GITHUB_TOKEN],
 ] as const);
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
diff --git a/tests/t081-cross-platform-receipt-golden.test.ts b/tests/t081-cross-platform-receipt-golden.test.ts
index 7d07b37..fd6d0c3 100644
--- a/tests/t081-cross-platform-receipt-golden.test.ts
+++ b/tests/t081-cross-platform-receipt-golden.test.ts
@@ -8,7 +8,7 @@ import { readGitHeadState, readWorkingTreeComparison } from "../src/git.js";
 import { validateReceiptSemantics, type ReceiptV1 } from "../src/receipt/model.js";
 
 const temporaryDirectories: string[] = [];
-const NULL_GIT_CONFIG = process.platform === "win32" ? "NUL" : "/dev/null";
+const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
 const GIT_ENV = {
   ...process.env,
   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
```

## Full file at head: tests/cli.smoke.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { join } from "node:path";
    5| import { afterEach, describe, expect, it, vi } from "vitest";
    6| 
    7| const ADMISSION_FLAG = "--allow-changed-command-surface";
    8| const ENV_KEYS = [
    9|   "ASCOUT_AGENT",
   10|   "ASCOUT_ALLOW_CHANGED_COMMAND_SURFACE",
   11|   "ASCOUT_CONFIG",
   12|   "ASCOUT_TOKEN",
   13|   "GH_TOKEN",
   14|   "GITHUB_TOKEN",
   15|   "NPM_TOKEN",
   16| ] as const;
   17| 
   18| const originalCwd = process.cwd();
   19| const originalEnv = new Map(ENV_KEYS.map((key) => [key, process.env[key]]));
   20| const temporaryDirectories: string[] = [];
   21| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   22| const GIT_ENV = {
   23|   ...process.env,
   24|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   25|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   26|   GIT_TERMINAL_PROMPT: "0",
   27| };
   28| 
   29| function git(repositoryRoot: string, argv: readonly string[]): string {
   30|   return execFileSync("git", [...argv], {
   31|     cwd: repositoryRoot,
   32|     encoding: "utf8",
   33|     env: GIT_ENV,
   34|     windowsHide: true,
   35|   });
   36| }
   37| 
   38| afterEach(() => {
   39|   process.chdir(originalCwd);
   40| 
   41|   for (const key of ENV_KEYS) {
   42|     const originalValue = originalEnv.get(key);
   43|     if (originalValue === undefined) {
   44|       delete process.env[key];
   45|     } else {
   46|       process.env[key] = originalValue;
   47|     }
   48|   }
   49| 
   50|   for (const directory of temporaryDirectories.splice(0)) {
   51|     rmSync(directory, { recursive: true, force: true });
   52|   }
   53| 
   54|   vi.restoreAllMocks();
   55|   vi.unstubAllGlobals();
   56|   vi.resetModules();
   57| });
   58| 
   59| describe("T007 CLI startup smoke", () => {
   60|   it("starts without network, account credentials, or project config", async () => {
   61|     const emptyProject = mkdtempSync(join(tmpdir(), "ascout-t007-"));
   62|     temporaryDirectories.push(emptyProject);
   63|     process.chdir(emptyProject);
   64| 
   65|     for (const key of ENV_KEYS) {
   66|       delete process.env[key];
   67|     }
   68| 
   69|     const fetchSpy = vi.fn(() => {
   70|       throw new Error("network access attempted during CLI startup");
   71|     });
   72|     vi.stubGlobal("fetch", fetchSpy);
   73|     const errorSpy = vi.spyOn(console, "error").mockImplementation(() => undefined);
   74| 
   75|     vi.resetModules();
   76|     const { runCli } = await import("../src/cli.js");
   77|     const exitCode = await runCli(["doctor"]);
   78|     const output = errorSpy.mock.calls.flat().map(String).join("\n");
   79| 
   80|     expect(typeof exitCode).toBe("number");
   81|     expect(exitCode).not.toBe(0);
   82|     expect(fetchSpy).not.toHaveBeenCalled();
   83|     expect(output).not.toContain(emptyProject);
   84|     expect(readdirSync(emptyProject)).toEqual([]);
   85|   });
   86| 
   87|   it("does not infer changed-command admission from agent or environment context", async () => {
   88|     process.env.ASCOUT_AGENT = "1";
   89|     process.env.ASCOUT_ALLOW_CHANGED_COMMAND_SURFACE = "1";
   90|     process.env.ASCOUT_TOKEN = "present-but-irrelevant";
   91|     process.env.GITHUB_TOKEN = "present-but-irrelevant";
   92| 
   93|     vi.resetModules();
   94|     const { parseCliArgs } = await import("../src/cli.js");
   95| 
   96|     expect(parseCliArgs(["check"])).toEqual({
   97|       command: "check",
   98|       allowChangedCommandSurface: false,
   99|     });
  100| 
  101|     expect(parseCliArgs(["check", ADMISSION_FLAG])).toEqual({
  102|       command: "check",
  103|       allowChangedCommandSurface: true,
  104|     });
  105|   });
  106| 
  107|   it("keeps init limited to config plus .gitignore and does not pre-create runtime state", async () => {
  108|     const emptyProject = mkdtempSync(join(tmpdir(), "ascout-t043-"));
  109|     temporaryDirectories.push(emptyProject);
  110|     process.chdir(emptyProject);
  111|     vi.spyOn(console, "error").mockImplementation(() => undefined);
  112| 
  113|     vi.resetModules();
  114|     const { runCli } = await import("../src/cli.js");
  115|     const exitCode = await runCli(["init"]);
  116| 
  117|     expect(exitCode).toBe(0);
  118|     expect(readdirSync(emptyProject).sort()).toEqual([".gitignore", "ascout.config.json"]);
  119|     expect(readFileSync(join(emptyProject, "ascout.config.json"), "utf8")).toBe(
  120|       JSON.stringify({ version: 1 }, null, 2),
  121|     );
  122|     expect(readFileSync(join(emptyProject, ".gitignore"), "utf8")).toBe(".ascout/");
  123|   });
  124| 
  125|   it("keeps doctor output opaque to local and repository-relative paths plus configured command secrets", async () => {
  126|     const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-t042-"));
  127|     temporaryDirectories.push(repositoryRoot);
  128|     process.chdir(repositoryRoot);
  129| 
  130|     git(repositoryRoot, ["init", "-q"]);
  131|     git(repositoryRoot, ["config", "core.autocrlf", "false"]);
  132| 
  133|     const secret = "doctor-must-not-render-this-secret";
  134|     writeFileSync(
  135|       join(repositoryRoot, "ascout.config.json"),
  136|       JSON.stringify({
  137|         version: 1,
  138|         tasks: {
  139|           lint: { command: ["custom-lint", "--token", secret] },
  140|         },
  141|       }),
  142|       "utf8",
  143|     );
  144|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n", "utf8");
  145|     git(repositoryRoot, ["add", "--all"]);
  146|     git(repositoryRoot, [
  147|       "-c",
  148|       "user.name=Ascout Test",
  149|       "-c",
  150|       "user.email=ascout@example.invalid",
  151|       "-c",
  152|       "commit.gpgsign=false",
  153|       "commit",
  154|       "-q",
  155|       "-m",
  156|       "base",
  157|     ]);
  158| 
  159|     const sensitiveChangedPath = "customer-acquisition-secret-plan.txt";
  160|     writeFileSync(join(repositoryRoot, sensitiveChangedPath), "private\n", "utf8");
  161| 
  162|     const errorSpy = vi.spyOn(console, "error").mockImplementation(() => undefined);
  163|     vi.resetModules();
  164|     const { runCli } = await import("../src/cli.js");
  165|     const exitCode = await runCli(["doctor"]);
  166|     const output = errorSpy.mock.calls.flat().map(String).join("\n");
  167| 
  168|     expect(exitCode).toBe(0);
  169|     expect(output).toContain("Repository identity: local:");
  170|     expect(output).toContain("Config source: repository_config");
  171|     expect(output).toContain("authorityPathCount:");
  172|     expect(output).toContain("Changed Files");
  173|     expect(output).not.toContain(repositoryRoot);
  174|     expect(output).not.toContain(secret);
  175|     expect(output).not.toContain("ascout.config.json");
  176|     expect(output).not.toContain(sensitiveChangedPath);
  177|   });
  178| });
```

## Full file at head: tests/drift.contract.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { join } from "node:path";
    5| 
    6| import { afterEach, describe, expect, it } from "vitest";
    7| 
    8| import { readTreeDigestV1 } from "../src/git.js";
    9| import { buildReceipt } from "../src/receipt/build.js";
   10| import { validateReceiptSemantics, type SourceStateV1 } from "../src/receipt/model.js";
   11| 
   12| const temporaryDirectories: string[] = [];
   13| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   14| const GIT_TEST_ENV = {
   15|   ...process.env,
   16|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   17|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   18|   GIT_TERMINAL_PROMPT: "0",
   19| };
   20| 
   21| function git(repositoryRoot: string, argv: readonly string[]): string {
   22|   return execFileSync("git", [...argv], {
   23|     cwd: repositoryRoot,
   24|     encoding: "utf8",
   25|     env: GIT_TEST_ENV,
   26|     windowsHide: true,
   27|   });
   28| }
   29| 
   30| function makeRepository(): string {
   31|   const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-t058-"));
   32|   temporaryDirectories.push(repositoryRoot);
   33|   execFileSync("git", ["init", "-q"], {
   34|     cwd: repositoryRoot,
   35|     env: GIT_TEST_ENV,
   36|     windowsHide: true,
   37|   });
   38|   git(repositoryRoot, ["config", "user.name", "Ascout Test"]);
   39|   git(repositoryRoot, ["config", "user.email", "ascout@example.invalid"]);
   40|   git(repositoryRoot, ["config", "commit.gpgSign", "false"]);
   41|   git(repositoryRoot, ["config", "core.autocrlf", "false"]);
   42|   return repositoryRoot;
   43| }
   44| 
   45| function commitAll(repositoryRoot: string, message: string): void {
   46|   git(repositoryRoot, ["add", "--all"]);
   47|   git(repositoryRoot, ["commit", "-q", "-m", message]);
   48| }
   49| 
   50| function sourceState(treeDigest: string): SourceStateV1 {
   51|   return {
   52|     repository_id: `local:${"a".repeat(64)}`,
   53|     repository_id_kind: "local_only",
   54|     portable: false,
   55|     head_sha: "b".repeat(40),
   56|     detached: false,
   57|     shallow: false,
   58|     tree_digest_version: 1,
   59|     tree_digest: treeDigest,
   60|     tracked_index_entry_count: 1,
   61|     unstaged_changed_count: 1,
   62|     included_untracked_count: 0,
   63|   };
   64| }
   65| 
   66| afterEach(() => {
   67|   for (const directory of temporaryDirectories.splice(0)) {
   68|     rmSync(directory, { recursive: true, force: true });
   69|   }
   70| });
   71| 
   72| describe("T058 source drift detection", () => {
   73|   it("changes tree_digest_v1 when tracked worktree content mutates after the start snapshot", () => {
   74|     const repositoryRoot = makeRepository();
   75|     writeFileSync(join(repositoryRoot, "tracked.txt"), "start\n");
   76|     commitAll(repositoryRoot, "base");
   77| 
   78|     const start = readTreeDigestV1(repositoryRoot);
   79|     expect(start.unstaged_changed_count).toBe(0);
   80| 
   81|     writeFileSync(join(repositoryRoot, "tracked.txt"), "mutated\n");
   82|     const end = readTreeDigestV1(repositoryRoot);
   83| 
   84|     expect(end.unstaged_changed_count).toBe(1);
   85|     expect(end.tree_digest).not.toBe(start.tree_digest);
   86|   });
   87| 
   88|   it("detects mutation of included untracked content while excluding .ascout runtime writes", () => {
   89|     const repositoryRoot = makeRepository();
   90|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
   91|     commitAll(repositoryRoot, "base");
   92| 
   93|     writeFileSync(join(repositoryRoot, "notes.txt"), "start\n");
   94|     const start = readTreeDigestV1(repositoryRoot);
   95|     expect(start.included_untracked_count).toBe(1);
   96| 
   97|     mkdirSync(join(repositoryRoot, ".ascout", "runs", "r1"), { recursive: true });
   98|     writeFileSync(join(repositoryRoot, ".ascout", "runs", "r1", "stdout.txt"), "runtime one\n");
   99|     const withRuntimeOutput = readTreeDigestV1(repositoryRoot);
  100|     expect(withRuntimeOutput).toEqual(start);
  101| 
  102|     writeFileSync(join(repositoryRoot, ".ascout", "runs", "r1", "stdout.txt"), "runtime two\n");
  103|     expect(readTreeDigestV1(repositoryRoot)).toEqual(start);
  104| 
  105|     writeFileSync(join(repositoryRoot, "notes.txt"), "mutated\n");
  106|     const end = readTreeDigestV1(repositoryRoot);
  107|     expect(end.included_untracked_count).toBe(1);
  108|     expect(end.tree_digest).not.toBe(start.tree_digest);
  109|   }, 15_000);
  110| });
  111| 
  112| describe("T058 drift exit contract", () => {
  113|   it("maps a valid tree-drifted receipt to exit 3 ahead of a remaining exercise gap", () => {
  114|     const start = sourceState("c".repeat(64));
  115|     const end = sourceState("d".repeat(64));
  116| 
  117|     const receipt = buildReceipt({
  118|       run: {
  119|         run_id: "run-t058-drift",
  120|         ascout_version: "0.1.0-m1",
  121|         started_at: "2026-08-27T10:30:00.000Z",
  122|         finished_at: "2026-08-27T10:30:01.000Z",
  123|         config_digest: "e".repeat(64),
  124|       },
  125|       sourceStart: start,
  126|       sourceEnd: end,
  127|       comparison: {
  128|         kind: "working_tree_vs_head",
  129|         base_ref: start.head_sha,
  130|         includes_staged: true,
  131|         includes_unstaged: true,
  132|         includes_untracked_nonignored: true,
  133|         changed_files: [{
  134|           path: "src/a.ts",
  135|           change_kind: "modified",
  136|           line_semantics: "text",
  137|           changed_new_line_ranges: [[10, 10]],
  138|           is_test_file: false,
  139|           is_snapshot: false,
  140|           is_command_surface: false,
  141|         }],
  142|       },
  143|       selection: {
  144|         mode: "native_related",
  145|         initial_scope: { kind: "repository", path: null },
  146|         selected_test_count: 1,
  147|         deselected_test_count: 0,
  148|         total_test_count: 1,
  149|         widened: false,
  150|         widen_triggers: [],
  151|         passes: [{
  152|           ordinal: 1,
  153|           mode: "native_related",
  154|           scope: { kind: "repository", path: null },
  155|           trigger: null,
  156|           selected_test_count: 1,
  157|           deselected_test_count: 0,
  158|           total_test_count: 1,
  159|         }],
  160|         limitations: [],
  161|       },
  162|       tasks: [{
  163|         task_id: "test-1",
  164|         task_type: "test",
  165|         authorized_by: "discovery",
  166|         source_path: "package.json",
  167|         argv: ["vitest", "related", "src/a.ts", "--run"],
  168|         argv_redacted: false,
  169|         tool_name: "vitest",
  170|         tool_version: "4.1.10",
  171|         command_surface_changed: false,
  172|         changed_authority_paths: [],
  173|         execution_admission: "normal",
  174|         status: "PASS",
  175|         reason_code: null,
  176|         reason_text: null,
  177|         exit_code: 0,
  178|         started_at: "2026-08-27T10:30:00.000Z",
  179|         finished_at: "2026-08-27T10:30:01.000Z",
  180|         duration_ms: 1_000,
  181|         observations: { runs: 1, failures: 0 },
  182|         cache_state: "cold",
  183|         evidence_ids: ["coverage-1"],
  184|         artifact_refs: [],
  185|         output_truncated: false,
  186|       }],
  187|       exercise: {
  188|         changed_executable_lines: 1,
  189|         exercised_lines: 0,
  190|         not_exercised_lines: 1,
  191|         unresolved_lines: 0,
  192|         changed_files_with_zero_exercised_lines: 1,
  193|         records: [{
  194|           path: "src/a.ts",
  195|           line: 10,
  196|           state: "NOT_EXERCISED",
  197|           execution_count: 0,
  198|           source_task_ids: ["test-1"],
  199|         }],
  200|       },
  201|       testChanges: [],
  202|       findings: [],
  203|       evidence: [{
  204|         evidence_id: "coverage-1",
  205|         run_id: "run-t058-drift",
  206|         task_id: "test-1",
  207|         sequence: 1,
  208|         kind: "coverage",
  209|         sha256: "f".repeat(64),
  210|         artifact_id: null,
  211|         redacted: false,
  212|         truncated: false,
  213|       }],
  214|       artifacts: [],
  215|     });
  216| 
  217|     expect(receipt.stability).toBe("tree_drifted");
  218|     expect(receipt.summary.completeness).toBe("materially_incomplete");
  219|     expect(receipt.summary.exit_code).toBe(3);
  220|     expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  221|   });
  222| });
```

## Full file at head: tests/git-diff.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import {
    3|   chmodSync,
    4|   mkdirSync,
    5|   mkdtempSync,
    6|   rmSync,
    7|   symlinkSync,
    8|   writeFileSync,
    9| } from "node:fs";
   10| import { tmpdir } from "node:os";
   11| import { join } from "node:path";
   12| import { afterEach, describe, expect, it } from "vitest";
   13| import {
   14|   GitIdentityError,
   15|   readWorkingTreeComparison,
   16|   type GitChangedFile,
   17| } from "../src/git.js";
   18| 
   19| const temporaryDirectories: string[] = [];
   20| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   21| const GIT_ENV = {
   22|   ...process.env,
   23|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   24|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   25|   GIT_TERMINAL_PROMPT: "0",
   26| };
   27| 
   28| function git(repositoryRoot: string, argv: readonly string[]): string {
   29|   return execFileSync("git", [...argv], {
   30|     cwd: repositoryRoot,
   31|     encoding: "utf8",
   32|     env: GIT_ENV,
   33|     windowsHide: true,
   34|   });
   35| }
   36| 
   37| function makeRepository(): string {
   38|   const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-t020-"));
   39|   temporaryDirectories.push(repositoryRoot);
   40|   git(repositoryRoot, ["init", "-q"]);
   41|   git(repositoryRoot, ["config", "user.name", "Ascout Test"]);
   42|   git(repositoryRoot, ["config", "user.email", "ascout@example.invalid"]);
   43|   git(repositoryRoot, ["config", "commit.gpgsign", "false"]);
   44|   git(repositoryRoot, ["config", "core.autocrlf", "false"]);
   45|   git(repositoryRoot, ["config", "core.excludesFile", join(repositoryRoot, ".empty-excludes")]);
   46|   git(repositoryRoot, ["config", "core.attributesFile", join(repositoryRoot, ".empty-attributes")]);
   47|   git(repositoryRoot, ["config", "core.hooksPath", join(repositoryRoot, ".empty-hooks")]);
   48|   writeFileSync(join(repositoryRoot, ".empty-excludes"), "");
   49|   writeFileSync(join(repositoryRoot, ".empty-attributes"), "");
   50|   mkdirSync(join(repositoryRoot, ".empty-hooks"));
   51|   return repositoryRoot;
   52| }
   53| 
   54| function commitAll(repositoryRoot: string, message = "base"): string {
   55|   git(repositoryRoot, ["add", "--all"]);
   56|   git(repositoryRoot, ["commit", "-q", "-m", message]);
   57|   return git(repositoryRoot, ["rev-parse", "HEAD"]).trim();
   58| }
   59| 
   60| function byPath(changed: readonly GitChangedFile[]): Map<string, GitChangedFile> {
   61|   return new Map(changed.map((entry) => [entry.path, entry]));
   62| }
   63| 
   64| function expectPositiveOrderedRanges(entry: GitChangedFile): void {
   65|   for (const [start, end] of entry.changed_new_line_ranges) {
   66|     expect(Number.isInteger(start)).toBe(true);
   67|     expect(Number.isInteger(end)).toBe(true);
   68|     expect(start).toBeGreaterThanOrEqual(1);
   69|     expect(end).toBeGreaterThanOrEqual(start);
   70|   }
   71| }
   72| 
   73| afterEach(() => {
   74|   for (const directory of temporaryDirectories.splice(0)) {
   75|     rmSync(directory, { recursive: true, force: true });
   76|   }
   77| });
   78| 
   79| describe("T020 working-tree changed scope", () => {
   80|   it("returns an exact clean comparison bound to source-start HEAD", () => {
   81|     const repositoryRoot = makeRepository();
   82|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
   83|     const head = commitAll(repositoryRoot);
   84| 
   85|     expect(readWorkingTreeComparison(repositoryRoot, head)).toEqual({
   86|       kind: "working_tree_vs_head",
   87|       base_ref: head,
   88|       includes_staged: true,
   89|       includes_unstaged: true,
   90|       includes_untracked_nonignored: true,
   91|       changed_files: [],
   92|     });
   93|   });
   94| 
   95|   it("covers tracked add/modify/delete/rename plus nonignored untracked scope", () => {
   96|     const repositoryRoot = makeRepository();
   97|     mkdirSync(join(repositoryRoot, "src"));
   98|     mkdirSync(join(repositoryRoot, ".ascout"));
   99|     writeFileSync(join(repositoryRoot, ".gitignore"), "ignored.txt\n");
  100|     writeFileSync(join(repositoryRoot, "src", "modified.txt"), "one\ntwo\nthree\n");
  101|     writeFileSync(join(repositoryRoot, "deleted.txt"), "gone\n");
  102|     writeFileSync(join(repositoryRoot, "rename-old.txt"), "alpha\nbeta\n");
  103|     writeFileSync(join(repositoryRoot, "binary.dat"), Buffer.from([1, 0, 2, 3]));
  104|     writeFileSync(join(repositoryRoot, ".ascout", "tracked.txt"), "tracked-base\n");
  105|     writeFileSync(join(repositoryRoot, "marker.txt"), "before\n");
  106|     const head = commitAll(repositoryRoot);
  107| 
  108|     writeFileSync(join(repositoryRoot, "src", "modified.txt"), "one\nTWO\nTHREE\n");
  109|     writeFileSync(join(repositoryRoot, "added.txt"), "a\nb\n");
  110|     git(repositoryRoot, ["add", "added.txt"]);
  111|     rmSync(join(repositoryRoot, "deleted.txt"));
  112|     git(repositoryRoot, ["mv", "rename-old.txt", "rename-new.txt"]);
  113|     writeFileSync(join(repositoryRoot, "binary.dat"), Buffer.from([1, 0, 8, 9]));
  114|     writeFileSync(
  115|       join(repositoryRoot, "marker.txt"),
  116|       "GIT binary patch\nBinary files a/x and b/y differ\n",
  117|     );
  118|     writeFileSync(join(repositoryRoot, ".ascout", "tracked.txt"), "tracked-change\n");
  119|     mkdirSync(join(repositoryRoot, "notes"));
  120|     writeFileSync(join(repositoryRoot, "notes", "new.txt"), "alpha\nbeta\ngamma");
  121|     writeFileSync(join(repositoryRoot, "notes", "empty.txt"), "");
  122|     writeFileSync(join(repositoryRoot, "notes", "binary.bin"), Buffer.from([9, 0, 8]));
  123|     writeFileSync(join(repositoryRoot, "notes", "large.txt"), "x".repeat(1024 * 1024 + 1));
  124|     writeFileSync(join(repositoryRoot, "ignored.txt"), "ignored\n");
  125|     writeFileSync(join(repositoryRoot, ".ascout", "runtime.json"), "{}\n");
  126| 
  127|     const comparison = readWorkingTreeComparison(repositoryRoot, head);
  128|     const changed = byPath(comparison.changed_files);
  129| 
  130|     expect(comparison.base_ref).toBe(head);
  131|     expect(changed.get("added.txt")).toEqual({
  132|       path: "added.txt",
  133|       change_kind: "added",
  134|       line_semantics: "text",
  135|       changed_new_line_ranges: [[1, 2]],
  136|     });
  137|     expect(changed.get("src/modified.txt")?.changed_new_line_ranges).toEqual([[2, 3]]);
  138|     expect(changed.get("deleted.txt")).toEqual({
  139|       path: "deleted.txt",
  140|       change_kind: "deleted",
  141|       line_semantics: "deleted_only",
  142|       changed_new_line_ranges: [],
  143|     });
  144|     expect(changed.get("rename-new.txt")).toEqual({
  145|       path: "rename-new.txt",
  146|       previous_path: "rename-old.txt",
  147|       change_kind: "renamed",
  148|       line_semantics: "text",
  149|       changed_new_line_ranges: [],
  150|     });
  151|     expect(changed.get("binary.dat")?.line_semantics).toBe("binary_or_non_line");
  152|     expect(changed.get("binary.dat")?.changed_new_line_ranges).toEqual([]);
  153|     expect(changed.get("marker.txt")?.line_semantics).toBe("text");
  154|     expect(changed.get("marker.txt")?.changed_new_line_ranges).toEqual([[1, 2]]);
  155|     expect(changed.get("notes/new.txt")?.changed_new_line_ranges).toEqual([[1, 3]]);
  156|     expect(changed.get("notes/empty.txt")?.changed_new_line_ranges).toEqual([]);
  157|     expect(changed.get("notes/binary.bin")?.line_semantics).toBe("binary_or_non_line");
  158|     expect(changed.get("notes/large.txt")).toEqual({
  159|       path: "notes/large.txt",
  160|       change_kind: "untracked",
  161|       line_semantics: "text",
  162|       changed_new_line_ranges: [[1, 1]],
  163|     });
  164|     expect(changed.get(".ascout/tracked.txt")?.change_kind).toBe("modified");
  165|     expect(changed.has("ignored.txt")).toBe(false);
  166|     expect(changed.has(".ascout/runtime.json")).toBe(false);
  167| 
  168|     for (const entry of comparison.changed_files) expectPositiveOrderedRanges(entry);
  169|   }, 15_000);
  170| 
  171|   it("preserves leading U+FEFF in untracked path identity", () => {
  172|     const repositoryRoot = makeRepository();
  173|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
  174|     const head = commitAll(repositoryRoot);
  175|     const plainName = "name.txt";
  176|     const bomName = "\uFEFFname.txt";
  177| 
  178|     writeFileSync(join(repositoryRoot, plainName), "plain\n");
  179|     writeFileSync(join(repositoryRoot, bomName), "bom\n");
  180|     const changed = byPath(readWorkingTreeComparison(repositoryRoot, head).changed_files);
  181| 
  182|     expect(changed.has(plainName)).toBe(true);
  183|     expect(changed.has(bomName)).toBe(true);
  184|     expect(changed.size).toBe(2);
  185|   });
  186| 
  187|   it("uses net working-tree state when staged content is canceled back to HEAD", () => {
  188|     const repositoryRoot = makeRepository();
  189|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
  190|     const head = commitAll(repositoryRoot);
  191| 
  192|     writeFileSync(join(repositoryRoot, "tracked.txt"), "staged\n");
  193|     git(repositoryRoot, ["add", "tracked.txt"]);
  194|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
  195| 
  196|     expect(git(repositoryRoot, ["status", "--short", "tracked.txt"]).trim()).toBe("MM tracked.txt");
  197|     expect(readWorkingTreeComparison(repositoryRoot, head).changed_files).toEqual([]);
  198|   });
  199| 
  200|   it("rejects a comparison base that is not the exact source-start HEAD", () => {
  201|     const repositoryRoot = makeRepository();
  202|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
  203|     const firstHead = commitAll(repositoryRoot, "first");
  204|     writeFileSync(join(repositoryRoot, "tracked.txt"), "next\n");
  205|     const secondHead = commitAll(repositoryRoot, "second");
  206|     expect(secondHead).not.toBe(firstHead);
  207| 
  208|     expect(() => readWorkingTreeComparison(repositoryRoot, firstHead)).toThrowError(
  209|       expect.objectContaining<Partial<GitIdentityError>>({ code: "git_metadata_error" }),
  210|     );
  211|     expect(() => readWorkingTreeComparison(repositoryRoot, "HEAD")).toThrowError(
  212|       expect.objectContaining<Partial<GitIdentityError>>({ code: "invalid_head_identity" }),
  213|     );
  214|   }, 15_000);
  215| 
  216|   it.skipIf(process.platform === "win32")(
  217|     "keeps mode/type-only changes file-level without invented line ranges",
  218|     () => {
  219|       const repositoryRoot = makeRepository();
  220|       writeFileSync(join(repositoryRoot, "mode.sh"), "echo ok\n", { mode: 0o644 });
  221|       writeFileSync(join(repositoryRoot, "kind"), "file\n");
  222|       const head = commitAll(repositoryRoot);
  223| 
  224|       chmodSync(join(repositoryRoot, "mode.sh"), 0o755);
  225|       rmSync(join(repositoryRoot, "kind"));
  226|       symlinkSync("target", join(repositoryRoot, "kind"));
  227| 
  228|       const changed = byPath(readWorkingTreeComparison(repositoryRoot, head).changed_files);
  229|       expect(changed.get("mode.sh")?.change_kind).toBe("modified");
  230|       expect(changed.get("mode.sh")?.changed_new_line_ranges).toEqual([]);
  231|       expect(changed.get("kind")).toEqual({
  232|         path: "kind",
  233|         change_kind: "type_changed",
  234|         line_semantics: "binary_or_non_line",
  235|         changed_new_line_ranges: [],
  236|       });
  237|     },
  238|   );
  239| 
  240|   it.skipIf(process.platform === "win32")(
  241|     "keeps symlink-to-regular type changes file-level without parser drift",
  242|     () => {
  243|       const repositoryRoot = makeRepository();
  244|       symlinkSync("target", join(repositoryRoot, "kind"));
  245|       writeFileSync(join(repositoryRoot, "zz-after.txt"), "before\n");
  246|       const head = commitAll(repositoryRoot);
  247| 
  248|       rmSync(join(repositoryRoot, "kind"));
  249|       writeFileSync(join(repositoryRoot, "kind"), "regular\n");
  250|       writeFileSync(join(repositoryRoot, "zz-after.txt"), "after\n");
  251| 
  252|       const changed = byPath(readWorkingTreeComparison(repositoryRoot, head).changed_files);
  253|       expect(changed.get("kind")).toEqual({
  254|         path: "kind",
  255|         change_kind: "type_changed",
  256|         line_semantics: "binary_or_non_line",
  257|         changed_new_line_ranges: [],
  258|       });
  259|       expect(changed.get("zz-after.txt")?.change_kind).toBe("modified");
  260|       expect(changed.get("zz-after.txt")?.changed_new_line_ranges).toEqual([[1, 1]]);
  261|     },
  262|   );
  263| });
```

## Full file at head: tests/git-tree-digest-bom.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { join } from "node:path";
    5| import { afterEach, describe, expect, it } from "vitest";
    6| import { readTreeDigestV1 } from "../src/git.js";
    7| 
    8| const temporaryDirectories: string[] = [];
    9| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   10| const GIT_ENV = {
   11|   ...process.env,
   12|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   13|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   14|   GIT_TERMINAL_PROMPT: "0",
   15| };
   16| 
   17| function git(repositoryRoot: string, argv: readonly string[]): string {
   18|   return execFileSync("git", [...argv], {
   19|     cwd: repositoryRoot,
   20|     encoding: "utf8",
   21|     env: GIT_ENV,
   22|     windowsHide: true,
   23|   });
   24| }
   25| 
   26| function makeRepository(): string {
   27|   const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-t019-bom-"));
   28|   temporaryDirectories.push(repositoryRoot);
   29|   git(repositoryRoot, ["init", "-q"]);
   30|   git(repositoryRoot, ["config", "user.name", "Ascout Test"]);
   31|   git(repositoryRoot, ["config", "user.email", "ascout@example.invalid"]);
   32|   git(repositoryRoot, ["config", "commit.gpgsign", "false"]);
   33|   return repositoryRoot;
   34| }
   35| 
   36| afterEach(() => {
   37|   for (const directory of temporaryDirectories.splice(0)) {
   38|     rmSync(directory, { recursive: true, force: true });
   39|   }
   40| });
   41| 
   42| describe("T019 UTF-8 Git pathname preservation", () => {
   43|   it("keeps a leading U+FEFF distinct from the same pathname without it", () => {
   44|     const repositoryRoot = makeRepository();
   45|     const plainName = "name.txt";
   46|     const bomName = "\uFEFFname.txt";
   47| 
   48|     writeFileSync(join(repositoryRoot, plainName), "same-base\n");
   49|     writeFileSync(join(repositoryRoot, bomName), "same-base\n");
   50|     git(repositoryRoot, ["add", "--all"]);
   51|     git(repositoryRoot, ["commit", "-q", "-m", "base"]);
   52| 
   53|     const clean = readTreeDigestV1(repositoryRoot);
   54|     expect(clean.tracked_index_entry_count).toBe(2);
   55|     expect(clean.unstaged_changed_count).toBe(0);
   56| 
   57|     writeFileSync(join(repositoryRoot, bomName), "changed-bom-path\n");
   58|     const changed = readTreeDigestV1(repositoryRoot);
   59|     expect(changed.unstaged_changed_count).toBe(1);
   60|     expect(changed.tree_digest).not.toBe(clean.tree_digest);
   61|   }, process.platform === "win32" ? 30_000 : 5_000);
   62| });
```

## Full file at head: tests/git-tree-digest.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { createHash } from "node:crypto";
    3| import {
    4|   chmodSync,
    5|   mkdirSync,
    6|   mkdtempSync,
    7|   rmSync,
    8|   symlinkSync,
    9|   unlinkSync,
   10|   utimesSync,
   11|   writeFileSync,
   12| } from "node:fs";
   13| import { tmpdir } from "node:os";
   14| import { join } from "node:path";
   15| import { afterEach, describe, expect, it } from "vitest";
   16| import {
   17|   GitIdentityError,
   18|   readTreeDigestV1,
   19|   treeDigestV1FromState,
   20|   type TreeDigestIndexEntry,
   21|   type TreeDigestState,
   22|   type TreeDigestUntrackedEntry,
   23| } from "../src/git.js";
   24| 
   25| const HEAD = "a".repeat(40);
   26| const BASE_INDEX = [
   27|   { path: "src/app.ts", mode: "100644", oid: "1".repeat(40), stage: 0 },
   28|   { path: "tests/__snapshots__/ui.snap", mode: "100644", oid: "2".repeat(40), stage: 0 },
   29| ] as const;
   30| const temporaryDirectories: string[] = [];
   31| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   32| const GIT_TEST_ENV = {
   33|   ...process.env,
   34|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   35|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   36|   GIT_TERMINAL_PROMPT: "0",
   37| };
   38| 
   39| function sha256Text(value: string): string {
   40|   return createHash("sha256").update(value, "utf8").digest("hex");
   41| }
   42| 
   43| function cleanState(): TreeDigestState {
   44|   return { head: HEAD, index: BASE_INDEX, unstaged: [], untracked: [] };
   45| }
   46| 
   47| function git(repositoryRoot: string, argv: readonly string[]): string {
   48|   return execFileSync("git", [...argv], {
   49|     cwd: repositoryRoot,
   50|     encoding: "utf8",
   51|     env: GIT_TEST_ENV,
   52|     windowsHide: true,
   53|   });
   54| }
   55| 
   56| function makeRepository(): string {
   57|   const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-t019-"));
   58|   temporaryDirectories.push(repositoryRoot);
   59|   execFileSync("git", ["init", "-q"], {
   60|     cwd: repositoryRoot,
   61|     env: GIT_TEST_ENV,
   62|     windowsHide: true,
   63|   });
   64| 
   65|   git(repositoryRoot, ["config", "user.name", "Ascout Test"]);
   66|   git(repositoryRoot, ["config", "user.email", "ascout@example.invalid"]);
   67|   git(repositoryRoot, ["config", "commit.gpgSign", "false"]);
   68|   git(repositoryRoot, ["config", "core.autocrlf", "false"]);
   69| 
   70|   const emptyExcludes = join(repositoryRoot, ".git", "ascout-empty-excludes");
   71|   const emptyAttributes = join(repositoryRoot, ".git", "ascout-empty-attributes");
   72|   const emptyHooks = join(repositoryRoot, ".git", "ascout-empty-hooks");
   73|   writeFileSync(emptyExcludes, "");
   74|   writeFileSync(emptyAttributes, "");
   75|   mkdirSync(emptyHooks);
   76|   git(repositoryRoot, ["config", "core.excludesFile", emptyExcludes]);
   77|   git(repositoryRoot, ["config", "core.attributesFile", emptyAttributes]);
   78|   git(repositoryRoot, ["config", "core.hooksPath", emptyHooks]);
   79| 
   80|   return repositoryRoot;
   81| }
   82| 
   83| function commitAll(repositoryRoot: string, message: string): void {
   84|   git(repositoryRoot, ["add", "--all"]);
   85|   git(repositoryRoot, ["commit", "-q", "-m", message]);
   86| }
   87| 
   88| function readIndexEntries(repositoryRoot: string): TreeDigestIndexEntry[] {
   89|   const output = git(repositoryRoot, ["ls-files", "--stage"]);
   90|   if (output.length === 0) return [];
   91|   return output.trimEnd().split("\n").map((line) => {
   92|     const match = /^([0-7]{6}) ([a-f0-9]{40}|[a-f0-9]{64}) ([0-3])\t(.+)$/.exec(line);
   93|     if (match === null) throw new Error(`unexpected index fixture: ${line}`);
   94|     const mode = match[1];
   95|     const oid = match[2];
   96|     const stage = match[3];
   97|     const path = match[4];
   98|     if (mode === undefined || oid === undefined || stage === undefined || path === undefined) {
   99|       throw new Error(`incomplete index fixture: ${line}`);
  100|     }
  101|     return { path, mode, oid, stage: Number(stage) };
  102|   });
  103| }
  104| 
  105| afterEach(() => {
  106|   for (const directory of temporaryDirectories.splice(0)) {
  107|     rmSync(directory, { recursive: true, force: true });
  108|   }
  109| });
  110| 
  111| describe("T019 tree_digest_v1 canonicalization", () => {
  112|   it("matches every T010 golden and remains input-order invariant", () => {
  113|     const targetDigest = sha256Text("../lib/app.ts");
  114|     const untracked: readonly TreeDigestUntrackedEntry[] = [
  115|       { path: "notes.txt", type: "file", mode: "100644", digest: sha256Text("notes\n"), ignored: false },
  116|       { path: "scratch.bin", type: "file", mode: "100644", digest: sha256Text("\u0000\u0001"), ignored: false },
  117|       { path: "tmp/keep.json", type: "file", mode: "100644", digest: sha256Text("{}\n"), ignored: false },
  118|       { path: "ignored.log", type: "file", mode: "100644", digest: sha256Text("ignored\n"), ignored: true },
  119|       { path: ".ascout/runs/r1/out.txt", type: "file", mode: "100644", digest: sha256Text("run evidence\n"), ignored: false },
  120|     ];
  121|     const unicodeUntracked: readonly TreeDigestUntrackedEntry[] = [
  122|       { path: "é.txt", type: "file", mode: "100644", digest: sha256Text("e-acute"), ignored: false },
  123|       { path: "z.txt", type: "file", mode: "100644", digest: sha256Text("z"), ignored: false },
  124|       { path: "ä.txt", type: "file", mode: "100644", digest: sha256Text("a-umlaut"), ignored: false },
  125|       { path: "a.txt", type: "file", mode: "100644", digest: sha256Text("a"), ignored: false },
  126|     ];
  127| 
  128|     const cases: readonly [string, TreeDigestState, string][] = [
  129|       ["clean", cleanState(), "368364c24d47714d6645ff1b098160280d363451dd1bd594853e4ec3bdc3ad82"],
  130|       [
  131|         "staged",
  132|         { ...cleanState(), index: [{ ...BASE_INDEX[0], oid: "3".repeat(40) }, BASE_INDEX[1]] },
  133|         "e4c8566d6ae1633dc8472974ad1ed0e524334c4b0f878e4ca99bab68fa8fa5d6",
  134|       ],
  135|       [
  136|         "unstaged",
  137|         {
  138|           ...cleanState(),
  139|           unstaged: [{
  140|             path: "src/app.ts",
  141|             state: "modified",
  142|             type: "file",
  143|             mode: "100644",
  144|             digest: sha256Text("console.log('changed')\n"),
  145|           }],
  146|         },
  147|         "bd41af5b7e6c49b5dab8333428323143319b5425696cc04aa22f38a8e597e0a9",
  148|       ],
  149|       [
  150|         "deletion",
  151|         { ...cleanState(), unstaged: [{ path: "src/app.ts", state: "deleted" }] },
  152|         "d7f21bff1d9c29b0887654548ff1dc3c520e3109bbc93798a1a580cefae061fd",
  153|       ],
  154|       [
  155|         "symlink",
  156|         {
  157|           ...cleanState(),
  158|           unstaged: [{
  159|             path: "src/app.ts",
  160|             state: "modified",
  161|             type: "symlink",
  162|             mode: "120000",
  163|             digest: targetDigest,
  164|           }],
  165|         },
  166|         "a591e715c4dfcd9adc1e3edda7070959b847ea5fc3b46874bda1513e5d524353",
  167|       ],
  168|       [
  169|         "mode",
  170|         {
  171|           ...cleanState(),
  172|           unstaged: [{
  173|             path: "src/app.ts",
  174|             state: "modified",
  175|             type: "file",
  176|             mode: "100755",
  177|             digest: sha256Text("console.log('base')\n"),
  178|           }],
  179|         },
  180|         "42be8e0497be224db269b0f2da0f1a945b14f26661cdddfe82595cd3a48adb03",
  181|       ],
  182|       [
  183|         "type",
  184|         {
  185|           ...cleanState(),
  186|           unstaged: [{
  187|             path: "src/app.ts",
  188|             state: "type_changed",
  189|             type: "symlink",
  190|             mode: "120000",
  191|             digest: targetDigest,
  192|           }],
  193|         },
  194|         "018630f3aa90b43a1f0c9a6926dfbc2a1ce1e725754f57d49ea732f6c257c44d",
  195|       ],
  196|       [
  197|         "untracked",
  198|         { ...cleanState(), untracked },
  199|         "b1aab29b5e465e44224145254caa51b3f9f371f7e1414e3799a1f13ad9be6cc7",
  200|       ],
  201|       [
  202|         "unicode-untracked",
  203|         { ...cleanState(), untracked: unicodeUntracked },
  204|         "7955d13f9e3bf356f2a34c5e3180e2e0c71b4c26001ccd4024ffccbbff3c0925",
  205|       ],
  206|       [
  207|         "snapshot",
  208|         {
  209|           ...cleanState(),
  210|           unstaged: [{
  211|             path: "tests/__snapshots__/ui.snap",
  212|             state: "modified",
  213|             type: "file",
  214|             mode: "100644",
  215|             digest: sha256Text('exports[`ui`] = `"changed"`;\n'),
  216|           }],
  217|         },
  218|         "08ed4832503efb7087fc38de9558a20409fc692085eb694475abffa89ff7c59d",
  219|       ],
  220|     ];
  221| 
  222|     for (const [name, state, expected] of cases) {
  223|       const digest = treeDigestV1FromState(state);
  224|       expect(digest.tree_digest, name).toBe(expected);
  225|       expect(digest.tree_digest_version).toBe(1);
  226|     }
  227| 
  228|     const reordered = treeDigestV1FromState({
  229|       ...cleanState(),
  230|       index: [...BASE_INDEX].reverse(),
  231|       untracked: [...unicodeUntracked].reverse(),
  232|     });
  233|     expect(reordered.tree_digest).toBe(
  234|       treeDigestV1FromState({ ...cleanState(), untracked: unicodeUntracked }).tree_digest,
  235|     );
  236|   });
  237| 
  238|   it("rejects non-canonical repository paths before hashing", () => {
  239|     expect(() => treeDigestV1FromState({
  240|       ...cleanState(),
  241|       index: [{ ...BASE_INDEX[0], path: "../escape.txt" }],
  242|     })).toThrow(GitIdentityError);
  243|     expect(() => treeDigestV1FromState({
  244|       ...cleanState(),
  245|       untracked: [{
  246|         path: "bad\\name.txt",
  247|         type: "file",
  248|         mode: "100644",
  249|         digest: sha256Text("bad"),
  250|         ignored: false,
  251|       }],
  252|     })).toThrow(GitIdentityError);
  253|   });
  254| });
  255| 
  256| describe("T019 live Git tree-digest collection", () => {
  257|   it("binds clean, staged, unstaged, deletion, and all nonignored untracked state", () => {
  258|     const repositoryRoot = makeRepository();
  259|     mkdirSync(join(repositoryRoot, "src"));
  260|     writeFileSync(join(repositoryRoot, "src", "app.ts"), "console.log('base')\n");
  261|     commitAll(repositoryRoot, "base");
  262| 
  263|     const clean = readTreeDigestV1(repositoryRoot);
  264|     expect(clean.tracked_index_entry_count).toBe(1);
  265|     expect(clean.unstaged_changed_count).toBe(0);
  266|     expect(clean.included_untracked_count).toBe(0);
  267| 
  268|     writeFileSync(join(repositoryRoot, "src", "app.ts"), "console.log('unstaged')\n");
  269|     const unstaged = readTreeDigestV1(repositoryRoot);
  270|     expect(unstaged.unstaged_changed_count).toBe(1);
  271|     expect(unstaged.tree_digest).not.toBe(clean.tree_digest);
  272| 
  273|     git(repositoryRoot, ["add", "src/app.ts"]);
  274|     const staged = readTreeDigestV1(repositoryRoot);
  275|     expect(staged.unstaged_changed_count).toBe(0);
  276|     expect(staged.tree_digest).not.toBe(clean.tree_digest);
  277|     expect(staged.tree_digest).not.toBe(unstaged.tree_digest);
  278| 
  279|     git(repositoryRoot, ["reset", "--hard", "HEAD"]);
  280|     unlinkSync(join(repositoryRoot, "src", "app.ts"));
  281|     const deleted = readTreeDigestV1(repositoryRoot);
  282|     expect(deleted.unstaged_changed_count).toBe(1);
  283|     expect(deleted.tree_digest).not.toBe(clean.tree_digest);
  284| 
  285|     git(repositoryRoot, ["checkout", "--", "src/app.ts"]);
  286|     writeFileSync(join(repositoryRoot, ".gitignore"), "ignored.log\n");
  287|     commitAll(repositoryRoot, "ignore");
  288|     const baseline = readTreeDigestV1(repositoryRoot);
  289| 
  290|     writeFileSync(join(repositoryRoot, "notes.txt"), "notes\n");
  291|     writeFileSync(join(repositoryRoot, "ignored.log"), "ignored\n");
  292|     mkdirSync(join(repositoryRoot, ".ascout", "runs", "r1"), { recursive: true });
  293|     writeFileSync(join(repositoryRoot, ".ascout", "runs", "r1", "out.txt"), "runtime\n");
  294|     const withUntracked = readTreeDigestV1(repositoryRoot);
  295|     expect(withUntracked.included_untracked_count).toBe(1);
  296|     expect(withUntracked.tree_digest).not.toBe(baseline.tree_digest);
  297| 
  298|     rmSync(join(repositoryRoot, "ignored.log"));
  299|     rmSync(join(repositoryRoot, ".ascout"), { recursive: true, force: true });
  300|     expect(readTreeDigestV1(repositoryRoot)).toEqual(withUntracked);
  301|   }, 15_000);
  302| 
  303|   it("filters stale-stat false modifications without refreshing the index", () => {
  304|     const repositoryRoot = makeRepository();
  305|     const tracked = join(repositoryRoot, "tracked.txt");
  306|     writeFileSync(tracked, "base\n");
  307|     commitAll(repositoryRoot, "base");
  308|     const clean = readTreeDigestV1(repositoryRoot);
  309| 
  310|     const future = new Date(Date.now() + 24 * 60 * 60 * 1000);
  311|     utimesSync(tracked, future, future);
  312|     expect(git(repositoryRoot, ["diff-files", "--raw", "--", "tracked.txt"])).toContain(
  313|       " M\ttracked.txt",
  314|     );
  315| 
  316|     expect(readTreeDigestV1(repositoryRoot)).toEqual(clean);
  317|   });
  318| 
  319|   it("fails closed when index visibility flags can hide tracked worktree state", () => {
  320|     const repositoryRoot = makeRepository();
  321|     writeFileSync(join(repositoryRoot, "tracked.txt"), "base\n");
  322|     commitAll(repositoryRoot, "base");
  323| 
  324|     git(repositoryRoot, ["update-index", "--assume-unchanged", "tracked.txt"]);
  325|     writeFileSync(join(repositoryRoot, "tracked.txt"), "hidden change\n");
  326|     expect(() => readTreeDigestV1(repositoryRoot)).toThrow(GitIdentityError);
  327| 
  328|     git(repositoryRoot, ["update-index", "--no-assume-unchanged", "tracked.txt"]);
  329|     git(repositoryRoot, ["checkout", "--", "tracked.txt"]);
  330|     git(repositoryRoot, ["update-index", "--skip-worktree", "tracked.txt"]);
  331|     writeFileSync(join(repositoryRoot, "tracked.txt"), "hidden skip-worktree change\n");
  332|     expect(() => readTreeDigestV1(repositoryRoot)).toThrow(GitIdentityError);
  333|   }, 15_000);
  334| 
  335|   it("names unmerged tracked state instead of treating it as malformed metadata", () => {
  336|     const repositoryRoot = makeRepository();
  337|     const originalBranch = git(repositoryRoot, ["symbolic-ref", "--short", "HEAD"]).trim();
  338|     writeFileSync(join(repositoryRoot, "conflict.txt"), "base\n");
  339|     commitAll(repositoryRoot, "base");
  340| 
  341|     git(repositoryRoot, ["checkout", "-q", "-b", "other"]);
  342|     writeFileSync(join(repositoryRoot, "conflict.txt"), "other\n");
  343|     commitAll(repositoryRoot, "other");
  344| 
  345|     git(repositoryRoot, ["checkout", "-q", originalBranch]);
  346|     writeFileSync(join(repositoryRoot, "conflict.txt"), "current\n");
  347|     commitAll(repositoryRoot, "current");
  348|     try {
  349|       git(repositoryRoot, ["merge", "--no-edit", "other"]);
  350|     } catch {
  351|       // Expected merge conflict fixture.
  352|     }
  353| 
  354|     expect(() => readTreeDigestV1(repositoryRoot)).toThrowError(/unmerged tracked state/);
  355|   }, 15_000);
  356| 
  357|   it("hashes regular files larger than one internal hash chunk", () => {
  358|     const repositoryRoot = makeRepository();
  359|     writeFileSync(join(repositoryRoot, "base.txt"), "base\n");
  360|     commitAll(repositoryRoot, "base");
  361|     const clean = readTreeDigestV1(repositoryRoot);
  362| 
  363|     writeFileSync(join(repositoryRoot, "large.bin"), Buffer.alloc(256 * 1024, 0x61));
  364|     const withLargeFile = readTreeDigestV1(repositoryRoot);
  365|     expect(withLargeFile.included_untracked_count).toBe(1);
  366|     expect(withLargeFile.tree_digest).not.toBe(clean.tree_digest);
  367|   });
  368| 
  369|   it("uses the Git owner-execute rule for untracked regular-file mode", () => {
  370|     if (process.platform === "win32") return;
  371| 
  372|     const repositoryRoot = makeRepository();
  373|     writeFileSync(join(repositoryRoot, "base.txt"), "base\n");
  374|     commitAll(repositoryRoot, "base");
  375|     writeFileSync(join(repositoryRoot, "mode.txt"), "mode\n");
  376|     chmodSync(join(repositoryRoot, "mode.txt"), 0o645);
  377| 
  378|     const expected = treeDigestV1FromState({
  379|       head: git(repositoryRoot, ["rev-parse", "HEAD"]).trim(),
  380|       index: readIndexEntries(repositoryRoot),
  381|       unstaged: [],
  382|       untracked: [{
  383|         path: "mode.txt",
  384|         type: "file",
  385|         mode: "100644",
  386|         digest: sha256Text("mode\n"),
  387|         ignored: false,
  388|       }],
  389|     });
  390|     expect(readTreeDigestV1(repositoryRoot)).toEqual(expected);
  391|   });
  392| 
  393|   it("binds executable mode and symlink target/type where the platform exposes them", () => {
  394|     const repositoryRoot = makeRepository();
  395|     writeFileSync(join(repositoryRoot, "tool.sh"), "#!/bin/sh\nexit 0\n");
  396|     commitAll(repositoryRoot, "base");
  397|     const clean = readTreeDigestV1(repositoryRoot);
  398| 
  399|     if (process.platform !== "win32") {
  400|       chmodSync(join(repositoryRoot, "tool.sh"), 0o755);
  401|       const executable = readTreeDigestV1(repositoryRoot);
  402|       expect(executable.unstaged_changed_count).toBe(1);
  403|       expect(executable.tree_digest).not.toBe(clean.tree_digest);
  404| 
  405|       chmodSync(join(repositoryRoot, "tool.sh"), 0o644);
  406|       unlinkSync(join(repositoryRoot, "tool.sh"));
  407|       symlinkSync("target.sh", join(repositoryRoot, "tool.sh"));
  408|       const typeChanged = readTreeDigestV1(repositoryRoot);
  409|       expect(typeChanged.unstaged_changed_count).toBe(1);
  410|       expect(typeChanged.tree_digest).not.toBe(clean.tree_digest);
  411|       expect(typeChanged.tree_digest).not.toBe(executable.tree_digest);
  412|     }
  413|   });
  414| });
```

## Full file at head: tests/pr41-p0-regressions.contract.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { join } from "node:path";
    5| import { afterEach, describe, expect, it } from "vitest";
    6| 
    7| import { runCheck } from "../src/check.js";
    8| import {
    9|   classifyCommandSurfaces,
   10|   discoverProjectFromFiles,
   11| } from "../src/discovery.js";
   12| import type { GitChangedFile } from "../src/git.js";
   13| import { planESLintTask } from "../src/tools/eslint.js";
   14| 
   15| const temporaryDirectories: string[] = [];
   16| const originalEnv = new Map([
   17|   ["ASCOUT_PR41_SECRET", process.env.ASCOUT_PR41_SECRET],
   18|   ["GITHUB_TOKEN", process.env.GITHUB_TOKEN],
   19| ] as const);
   20| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   21| const GIT_ENV = {
   22|   ...process.env,
   23|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   24|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   25|   GIT_TERMINAL_PROMPT: "0",
   26| };
   27| 
   28| function git(repositoryRoot: string, argv: readonly string[]): string {
   29|   return execFileSync("git", [...argv], {
   30|     cwd: repositoryRoot,
   31|     encoding: "utf8",
   32|     env: GIT_ENV,
   33|     windowsHide: true,
   34|   });
   35| }
   36| 
   37| function makeRepository(): string {
   38|   const repositoryRoot = mkdtempSync(join(tmpdir(), "ascout-pr41-"));
   39|   temporaryDirectories.push(repositoryRoot);
   40|   git(repositoryRoot, ["init", "-q"]);
   41|   git(repositoryRoot, ["config", "user.name", "Ascout Test"]);
   42|   git(repositoryRoot, ["config", "user.email", "ascout@example.invalid"]);
   43|   git(repositoryRoot, ["config", "commit.gpgsign", "false"]);
   44|   git(repositoryRoot, ["config", "core.autocrlf", "false"]);
   45|   writeFileSync(join(repositoryRoot, ".gitignore"), ".ascout/\n", "utf8");
   46|   return repositoryRoot;
   47| }
   48| 
   49| function commitAll(repositoryRoot: string, message = "base"): void {
   50|   git(repositoryRoot, ["add", "--all"]);
   51|   git(repositoryRoot, ["commit", "-q", "-m", message]);
   52| }
   53| 
   54| function changed(path: string): GitChangedFile {
   55|   return {
   56|     path,
   57|     change_kind: "modified",
   58|     line_semantics: "text",
   59|     changed_new_line_ranges: [[1, 1]],
   60|   };
   61| }
   62| 
   63| function packageJson(value: Record<string, unknown>): string {
   64|   return JSON.stringify(value);
   65| }
   66| 
   67| afterEach(() => {
   68|   for (const [name, value] of originalEnv) {
   69|     if (value === undefined) {
   70|       delete process.env[name];
   71|     } else {
   72|       process.env[name] = value;
   73|     }
   74|   }
   75|   for (const directory of temporaryDirectories.splice(0)) {
   76|     rmSync(directory, { recursive: true, force: true });
   77|   }
   78| });
   79| 
   80| describe("PR #41 P0 discovery regressions", () => {
   81|   it("does not fabricate a root package manifest in a package-less repository", () => {
   82|     const discovery = discoverProjectFromFiles({
   83|       "pyproject.toml": "[tool.pytest.ini_options]\naddopts = '-q'\n",
   84|       "examples/demo/package.json": packageJson({
   85|         name: "demo",
   86|         scripts: { lint: "eslint ." },
   87|       }),
   88|       "examples/demo/eslint.config.js": "export default [];\n",
   89|     });
   90| 
   91|     expect(discovery.workspace).toMatchObject({
   92|       state: "resolved",
   93|       kind: "single",
   94|       packageJsonPaths: [],
   95|     });
   96|     expect(discovery.packageManager.state).toBe("absent");
   97|     expect(discovery.tools.eslint.declarationPaths).toEqual([]);
   98|     expect(discovery.tools.eslint.configPaths).toEqual([]);
   99|     expect(discovery.packageScriptAuthority.lint).toEqual([]);
  100|   });
  101| 
  102|   it("keeps undeclared nested packages outside a single-package repository scope", () => {
  103|     const discovery = discoverProjectFromFiles({
  104|       "package.json": packageJson({
  105|         name: "root",
  106|         devDependencies: { eslint: "10.0.0" },
  107|       }),
  108|       "eslint.config.js": "export default [];\n",
  109|       "examples/demo/package.json": packageJson({
  110|         name: "demo",
  111|         scripts: { lint: "eslint ." },
  112|         devDependencies: { eslint: "10.0.0" },
  113|       }),
  114|       "examples/demo/eslint.config.js": "export default [];\n",
  115|     });
  116| 
  117|     expect(discovery.workspace.packageJsonPaths).toEqual(["package.json"]);
  118|     expect(discovery.tools.eslint.declarationPaths).toEqual(["package.json"]);
  119|     expect(discovery.tools.eslint.configPaths).toEqual(["eslint.config.js"]);
  120|     expect(discovery.packageScriptAuthority.lint).toEqual([]);
  121|   });
  122| 
  123|   it("treats only manifests that actually define or declare task authority as command surfaces", () => {
  124|     const discovery = discoverProjectFromFiles({
  125|       "package.json": packageJson({
  126|         name: "root",
  127|         workspaces: ["packages/*"],
  128|       }),
  129|       "packages/app/package.json": packageJson({
  130|         name: "app",
  131|         scripts: { lint: "eslint ." },
  132|       }),
  133|       "packages/docs/package.json": packageJson({ name: "docs" }),
  134|     });
  135|     const surfaces = classifyCommandSurfaces(discovery);
  136| 
  137|     expect(discovery.packageScriptAuthority.lint).toEqual(["packages/app/package.json"]);
  138|     expect(surfaces.lint.authorityPaths).toContain("packages/app/package.json");
  139|     expect(surfaces.lint.authorityPaths).not.toContain("packages/docs/package.json");
  140|   });
  141| });
  142| 
  143| describe("PR #41 P0 ESLint scope regression", () => {
  144|   it("does not use an unrelated workspace lint script to resolve multi-config ambiguity", () => {
  145|     const files = {
  146|       "package.json": packageJson({
  147|         name: "root",
  148|         private: true,
  149|         packageManager: "npm@11.0.0",
  150|         workspaces: ["packages/*"],
  151|         devDependencies: { eslint: "10.0.0" },
  152|       }),
  153|       "packages/app/package.json": packageJson({ name: "app" }),
  154|       "packages/other/package.json": packageJson({
  155|         name: "other",
  156|         scripts: { lint: "eslint ." },
  157|       }),
  158|       "packages/app/eslint.config.js": "export default [];\n",
  159|       "packages/other/eslint.config.js": "export default [];\n",
  160|       "node_modules/.bin/eslint": "virtual executable",
  161|     };
  162| 
  163|     const plan = planESLintTask({
  164|       config: { version: 1 },
  165|       discovery: discoverProjectFromFiles(files),
  166|       files,
  167|       changedFiles: [changed("packages/app/src/app.ts")],
  168|     });
  169| 
  170|     expect(plan).toMatchObject({
  171|       state: "not_run",
  172|       argv: [],
  173|       reasonCode: "config_ambiguous",
  174|     });
  175|     expect(plan.sourcePath).not.toBe("packages/other/package.json");
  176|   });
  177| });
  178| 
  179| describe("PR #41 P0 receipt integrity regressions", () => {
  180|   it("redacts selected secret values from admission-refused argv", async () => {
  181|     const repositoryRoot = makeRepository();
  182|     const secret = "pr41-super-secret-value";
  183|     process.env.ASCOUT_PR41_SECRET = secret;
  184| 
  185|     writeFileSync(
  186|       join(repositoryRoot, "ascout.config.json"),
  187|       JSON.stringify({ version: 1 }, null, 2),
  188|       "utf8",
  189|     );
  190|     commitAll(repositoryRoot);
  191| 
  192|     writeFileSync(
  193|       join(repositoryRoot, "ascout.config.json"),
  194|       JSON.stringify({
  195|         version: 1,
  196|         redactEnv: ["ASCOUT_PR41_SECRET"],
  197|         tasks: {
  198|           lint: { command: ["must-not-launch", secret] },
  199|         },
  200|       }, null, 2),
  201|       "utf8",
  202|     );
  203| 
  204|     const outcome = await runCheck(repositoryRoot);
  205|     const lint = outcome.receipt.tasks.find(({ task_type }) => task_type === "lint");
  206| 
  207|     expect(lint).toBeDefined();
  208|     expect(lint).toMatchObject({
  209|       status: "NOT_RUN",
  210|       execution_admission: "refused_changed_surface",
  211|       argv_redacted: true,
  212|     });
  213|     expect(lint!.argv.join("\n")).not.toContain(secret);
  214|     expect(lint!.argv).toEqual(["must-not-launch", ""]);
  215|   }, 15_000);
  216| 
  217|   it("redacts canonical built-in secrets from persisted argv and output without redactEnv", async () => {
  218|     const repositoryRoot = makeRepository();
  219|     const secret = "github-built-in-secret-value";
  220|     process.env.GITHUB_TOKEN = secret;
  221| 
  222|     writeFileSync(
  223|       join(repositoryRoot, "ascout.config.json"),
  224|       JSON.stringify({ version: 1 }, null, 2),
  225|       "utf8",
  226|     );
  227|     commitAll(repositoryRoot);
  228| 
  229|     writeFileSync(
  230|       join(repositoryRoot, "ascout.config.json"),
  231|       JSON.stringify({
  232|         version: 1,
  233|         tasks: {
  234|           lint: {
  235|             command: [
  236|               process.execPath,
  237|               "-e",
  238|               "process.stdout.write(process.env.GITHUB_TOKEN ?? '')",
  239|               secret,
  240|             ],
  241|           },
  242|         },
  243|       }, null, 2),
  244|       "utf8",
  245|     );
  246| 
  247|     const outcome = await runCheck(repositoryRoot, { allowChangedCommandSurface: true });
  248|     const lint = outcome.receipt.tasks.find(({ task_type }) => task_type === "lint");
  249|     const stdout = outcome.receipt.artifacts.find(
  250|       ({ task_id, relative_run_path }) =>
  251|         task_id === "lint" && relative_run_path === "raw/lint-stdout.log",
  252|     );
  253| 
  254|     expect(lint).toMatchObject({
  255|       status: "PASS",
  256|       argv_redacted: true,
  257|     });
  258|     expect(lint!.argv.join("\n")).not.toContain(secret);
  259|     expect(stdout).toMatchObject({
  260|       redacted: true,
  261|       truncated: false,
  262|       byte_length: 0,
  263|     });
  264|   }, 15_000);
  265| 
  266|   it("marks changed authority files as command surfaces in the same receipt", async () => {
  267|     const repositoryRoot = makeRepository();
  268|     writeFileSync(
  269|       join(repositoryRoot, "package.json"),
  270|       packageJson({
  271|         name: "fixture",
  272|         private: true,
  273|         packageManager: "npm@11.0.0",
  274|         scripts: { lint: "eslint ." },
  275|       }),
  276|       "utf8",
  277|     );
  278|     commitAll(repositoryRoot);
  279| 
  280|     writeFileSync(
  281|       join(repositoryRoot, "package.json"),
  282|       packageJson({
  283|         name: "fixture",
  284|         private: true,
  285|         version: "1.0.1",
  286|         packageManager: "npm@11.0.0",
  287|         scripts: { lint: "eslint ." },
  288|       }),
  289|       "utf8",
  290|     );
  291| 
  292|     const outcome = await runCheck(repositoryRoot);
  293|     const changedPackage = outcome.receipt.comparison.changed_files.find(
  294|       ({ path }) => path === "package.json",
  295|     );
  296|     const lint = outcome.receipt.tasks.find(({ task_type }) => task_type === "lint");
  297| 
  298|     expect(changedPackage).toMatchObject({
  299|       path: "package.json",
  300|       is_command_surface: true,
  301|     });
  302|     expect(lint).toMatchObject({
  303|       status: "NOT_RUN",
  304|       command_surface_changed: true,
  305|       changed_authority_paths: ["package.json"],
  306|       execution_admission: "refused_changed_surface",
  307|     });
  308|   }, 15_000);
  309| 
  310|   it("marks redacted output as redacted without fabricating truncation", async () => {
  311|     const repositoryRoot = makeRepository();
  312|     const secret = "pr41-output-secret-value";
  313|     process.env.ASCOUT_PR41_SECRET = secret;
  314| 
  315|     writeFileSync(
  316|       join(repositoryRoot, "ascout.config.json"),
  317|       JSON.stringify({ version: 1 }, null, 2),
  318|       "utf8",
  319|     );
  320|     commitAll(repositoryRoot);
  321| 
  322|     writeFileSync(
  323|       join(repositoryRoot, "ascout.config.json"),
  324|       JSON.stringify({
  325|         version: 1,
  326|         redactEnv: ["ASCOUT_PR41_SECRET"],
  327|         tasks: {
  328|           lint: {
  329|             command: [
  330|               process.execPath,
  331|               "-e",
  332|               "process.stdout.write(process.env.ASCOUT_PR41_SECRET ?? '')",
  333|             ],
  334|           },
  335|         },
  336|       }, null, 2),
  337|       "utf8",
  338|     );
  339| 
  340|     const outcome = await runCheck(repositoryRoot, { allowChangedCommandSurface: true });
  341|     const lint = outcome.receipt.tasks.find(({ task_type }) => task_type === "lint");
  342|     const stdout = outcome.receipt.artifacts.find(
  343|       ({ task_id, relative_run_path }) =>
  344|         task_id === "lint" && relative_run_path === "raw/lint-stdout.log",
  345|     );
  346|     const stdoutEvidence = outcome.receipt.evidence.find(
  347|       ({ artifact_id }) => artifact_id === stdout?.artifact_id,
  348|     );
  349| 
  350|     expect(lint?.status).toBe("PASS");
  351|     expect(lint?.output_truncated).toBe(false);
  352|     expect(stdout).toMatchObject({
  353|       redacted: true,
  354|       truncated: false,
  355|       byte_length: 0,
  356|     });
  357|     expect(stdoutEvidence).toMatchObject({
  358|       redacted: true,
  359|       truncated: false,
  360|     });
  361|   }, 15_000);
  362| 
  363|   it("binds run.started_at before an executed task starts", async () => {
  364|     const repositoryRoot = makeRepository();
  365|     writeFileSync(
  366|       join(repositoryRoot, "ascout.config.json"),
  367|       JSON.stringify({ version: 1 }, null, 2),
  368|       "utf8",
  369|     );
  370|     commitAll(repositoryRoot);
  371| 
  372|     writeFileSync(
  373|       join(repositoryRoot, "ascout.config.json"),
  374|       JSON.stringify({
  375|         version: 1,
  376|         tasks: {
  377|           lint: { command: [process.execPath, "-e", "process.exit(0)"] },
  378|         },
  379|       }, null, 2),
  380|       "utf8",
  381|     );
  382| 
  383|     const outcome = await runCheck(repositoryRoot, { allowChangedCommandSurface: true });
  384|     const lint = outcome.receipt.tasks.find(({ task_type }) => task_type === "lint");
  385| 
  386|     expect(lint?.status).toBe("PASS");
  387|     expect(lint?.started_at).not.toBeNull();
  388|     expect(Date.parse(outcome.receipt.run.started_at)).toBeLessThanOrEqual(
  389|       Date.parse(lint!.started_at!),
  390|     );
  391|   }, 15_000);
  392| });
```

## Full file at head: tests/t081-cross-platform-receipt-golden.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { join } from "node:path";
    5| import { afterEach, describe, expect, it } from "vitest";
    6| 
    7| import { readGitHeadState, readWorkingTreeComparison } from "../src/git.js";
    8| import { validateReceiptSemantics, type ReceiptV1 } from "../src/receipt/model.js";
    9| 
   10| const temporaryDirectories: string[] = [];
   11| const NULL_GIT_CONFIG = "/dev/null"; // Git for Windows accepts /dev/null; newer releases reject NUL.
   12| const GIT_ENV = {
   13|   ...process.env,
   14|   GIT_CONFIG_GLOBAL: NULL_GIT_CONFIG,
   15|   GIT_CONFIG_SYSTEM: NULL_GIT_CONFIG,
   16|   GIT_TERMINAL_PROMPT: "0",
   17| };
   18| const FIXED_GIT_DATES = {
   19|   GIT_AUTHOR_DATE: "2026-01-01T00:00:00Z",
   20|   GIT_COMMITTER_DATE: "2026-01-01T00:00:00Z",
   21| };
   22| 
   23| const HEAD_GOLDENS = {
   24|   sha1: "d06e36fb77c98e06d956405722ac8c065a5d1b74",
   25|   sha256: "94688a47c09cb0a184013e8e65d2f6062ad2d6f527546e39fe29ba8cfe8144da",
   26| } as const;
   27| 
   28| function git(repositoryRoot: string, argv: readonly string[], extraEnv: NodeJS.ProcessEnv = {}): string {
   29|   return execFileSync("git", [...argv], {
   30|     cwd: repositoryRoot,
   31|     encoding: "utf8",
   32|     env: { ...GIT_ENV, ...extraEnv },
   33|     windowsHide: true,
   34|   });
   35| }
   36| 
   37| function makeRepository(objectFormat: "sha1" | "sha256"): string {
   38|   const root = mkdtempSync(join(tmpdir(), `ascout-t081-${objectFormat}-`));
   39|   temporaryDirectories.push(root);
   40|   git(root, ["init", "-q", `--object-format=${objectFormat}`]);
   41|   git(root, ["config", "user.name", "Ascout T081"]);
   42|   git(root, ["config", "user.email", "t081@example.invalid"]);
   43|   git(root, ["config", "commit.gpgsign", "false"]);
   44|   git(root, ["config", "core.autocrlf", "false"]);
   45|   mkdirSync(join(root, "src"));
   46|   writeFileSync(join(root, "src", "a.ts"), "export const value = 1;\n", "utf8");
   47|   git(root, ["add", "src/a.ts"]);
   48|   git(root, ["commit", "-q", "-m", "fixture"], FIXED_GIT_DATES);
   49|   return root;
   50| }
   51| 
   52| function receiptFor(head: string): ReceiptV1 {
   53|   const tree = "b".repeat(64);
   54|   const source = {
   55|     repository_id: `local:${"c".repeat(64)}`,
   56|     repository_id_kind: "local_only" as const,
   57|     portable: false,
   58|     head_sha: head,
   59|     detached: false,
   60|     shallow: false,
   61|     tree_digest_version: 1 as const,
   62|     tree_digest: tree,
   63|     tracked_index_entry_count: 1,
   64|     unstaged_changed_count: 1,
   65|     included_untracked_count: 0,
   66|   };
   67|   return {
   68|     schema_version: "1.0",
   69|     run: {
   70|       run_id: "t081-run",
   71|       ascout_version: "0.1.0-m1",
   72|       started_at: "2026-01-01T00:00:00.000Z",
   73|       finished_at: "2026-01-01T00:00:01.000Z",
   74|       config_digest: "d".repeat(64),
   75|     },
   76|     source: { start: source, end: { ...source } },
   77|     comparison: {
   78|       kind: "working_tree_vs_head",
   79|       base_ref: head,
   80|       includes_staged: true,
   81|       includes_unstaged: true,
   82|       includes_untracked_nonignored: true,
   83|       changed_files: [{
   84|         path: "src/a.ts",
   85|         change_kind: "modified",
   86|         line_semantics: "text",
   87|         changed_new_line_ranges: [[1, 1]],
   88|         is_test_file: false,
   89|         is_snapshot: false,
   90|         is_command_surface: false,
   91|       }],
   92|     },
   93|     selection: {
   94|       mode: "no_test_task",
   95|       initial_scope: { kind: "repository", path: null },
   96|       selected_test_count: null,
   97|       deselected_test_count: null,
   98|       total_test_count: null,
   99|       widened: false,
  100|       widen_triggers: [],
  101|       passes: [],
  102|       limitations: ["t081 deterministic receipt fixture"],
  103|     },
  104|     tasks: [{
  105|       task_id: "lint-1",
  106|       task_type: "lint",
  107|       authorized_by: "discovery",
  108|       source_path: null,
  109|       argv: ["eslint", "src/a.ts"],
  110|       argv_redacted: false,
  111|       tool_name: "eslint",
  112|       tool_version: "1.0.0",
  113|       command_surface_changed: false,
  114|       changed_authority_paths: [],
  115|       execution_admission: "normal",
  116|       status: "PASS",
  117|       reason_code: null,
  118|       reason_text: null,
  119|       exit_code: 0,
  120|       started_at: "2026-01-01T00:00:00.000Z",
  121|       finished_at: "2026-01-01T00:00:01.000Z",
  122|       duration_ms: 1000,
  123|       observations: { runs: 1, failures: 0 },
  124|       cache_state: "cold",
  125|       evidence_ids: ["e1"],
  126|       artifact_refs: ["a1"],
  127|       output_truncated: false,
  128|     }],
  129|     changed_code: { changed_file_count: 1, changed_text_line_count: 1 },
  130|     exercise: {
  131|       changed_executable_lines: 0,
  132|       exercised_lines: 0,
  133|       not_exercised_lines: 0,
  134|       unresolved_lines: 0,
  135|       changed_files_with_zero_exercised_lines: 0,
  136|       records: [],
  137|     },
  138|     test_changes: [],
  139|     findings: [],
  140|     evidence: [{
  141|       evidence_id: "e1",
  142|       run_id: "t081-run",
  143|       task_id: "lint-1",
  144|       sequence: 1,
  145|       kind: "process_result",
  146|       sha256: "e".repeat(64),
  147|       artifact_id: "a1",
  148|       redacted: false,
  149|       truncated: false,
  150|     }],
  151|     artifacts: [{
  152|       artifact_id: "a1",
  153|       task_id: "lint-1",
  154|       relative_run_path: "raw/lint.txt",
  155|       kind: "stdout",
  156|       sha256: "f".repeat(64),
  157|       byte_length: 1,
  158|       redacted: false,
  159|       truncated: false,
  160|     }],
  161|     stability: "stable",
  162|     summary: {
  163|       task_status_counts: {
  164|         PASS: 1,
  165|         FAIL: 0,
  166|         FLAKY: 0,
  167|         BLOCKED: 0,
  168|         ERROR: 0,
  169|         NOT_APPLICABLE: 0,
  170|         NOT_RUN: 0,
  171|       },
  172|       finding_count: 0,
  173|       completeness: "complete",
  174|       exit_code: 0,
  175|     },
  176|   };
  177| }
  178| 
  179| function issueCodes(receipt: ReceiptV1): string[] {
  180|   return validateReceiptSemantics(receipt).issues.map(({ code }) => code);
  181| }
  182| 
  183| afterEach(() => {
  184|   for (const directory of temporaryDirectories.splice(0)) {
  185|     rmSync(directory, { recursive: true, force: true });
  186|   }
  187| });
  188| 
  189| describe("T081 cross-platform receipt goldens", () => {
  190|   for (const objectFormat of ["sha1", "sha256"] as const) {
  191|     it(`binds a deterministic real ${objectFormat.toUpperCase()} repository to one receipt identity`, () => {
  192|       const root = makeRepository(objectFormat);
  193|       const head = readGitHeadState(root);
  194|       expect(head.head_sha).toBe(HEAD_GOLDENS[objectFormat]);
  195|       expect(head.head_sha).toHaveLength(objectFormat === "sha1" ? 40 : 64);
  196| 
  197|       writeFileSync(join(root, "src", "a.ts"), "export const value = 2;\n", "utf8");
  198|       const comparison = readWorkingTreeComparison(root, head.head_sha);
  199|       expect(comparison.base_ref).toBe(head.head_sha);
  200|       expect(comparison.changed_files).toEqual([{
  201|         path: "src/a.ts",
  202|         change_kind: "modified",
  203|         line_semantics: "text",
  204|         changed_new_line_ranges: [[1, 1]],
  205|       }]);
  206| 
  207|       const receipt = receiptFor(head.head_sha);
  208|       expect(receipt.comparison.base_ref).toBe(receipt.source.start.head_sha);
  209|       expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  210|     });
  211|   }
  212| 
  213|   it("rejects raw path spellings before any repair and rejects inverted ranges", () => {
  214|     for (const invalid of [
  215|       "/src/a.ts",
  216|       "C:/repo/src/a.ts",
  217|       "\\\\server\\share\\a.ts",
  218|       "file:///src/a.ts",
  219|       "src\\a.ts",
  220|       "./src/a.ts",
  221|       "src/../a.ts",
  222|       "src//file.ts",
  223|       "src/",
  224|     ]) {
  225|       const receipt = receiptFor(HEAD_GOLDENS.sha1);
  226|       (receipt.comparison.changed_files[0] as { path: string }).path = invalid;
  227|       expect(issueCodes(receipt), invalid).toContain("noncanonical_original_path");
  228|     }
  229| 
  230|     const inverted = receiptFor(HEAD_GOLDENS.sha256);
  231|     (inverted.comparison.changed_files[0] as unknown as { changed_new_line_ranges: [number, number][] })
  232|       .changed_new_line_ranges = [[10, 1]];
  233|     (inverted.changed_code as { changed_text_line_count: number }).changed_text_line_count = 10;
  234|     const codes = issueCodes(inverted);
  235|     expect(codes).toContain("changed_range_inverted");
  236|     expect(codes).not.toContain("changed_text_line_count_mismatch");
  237|   });
  238| });
```
