You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad..e9617003ee7973ce90374bdfe7d5c8095a4695f8
Pull request title (context only): test(t107): build the simple Git fixture once per file and copy it
Changed files: tests/t107-self-verification-harness.contract.test.ts

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
- to: e9617003ee7973ce90374bdfe7d5c8095a4695f8
- merge_base: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- total_insertions: 21
- total_deletions: 6

~~- `tests/t107-self-verification-harness.contract.test.ts` [modified] +21/-6 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- tests/t107-self-verification-harness.contract.test.ts

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
diff --git a/tests/t107-self-verification-harness.contract.test.ts b/tests/t107-self-verification-harness.contract.test.ts
index 3ae5d90..89ab201 100644
--- a/tests/t107-self-verification-harness.contract.test.ts
+++ b/tests/t107-self-verification-harness.contract.test.ts
@@ -1,9 +1,9 @@
 import { execFileSync } from "node:child_process";
-import { existsSync, mkdirSync, mkdtempSync, promises as fsPromises, readFileSync, renameSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
+import { cpSync, existsSync, mkdirSync, mkdtempSync, promises as fsPromises, readFileSync, renameSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
 import { tmpdir } from "node:os";
 import { dirname, join } from "node:path";
 
-import { afterEach, describe, expect, it } from "vitest";
+import { afterAll, afterEach, describe, expect, it } from "vitest";
 
 import {
   SelfVerificationIntegrityError,
@@ -49,8 +49,7 @@ function git(root: string, args: readonly string[]): string {
   }).trim();
 }
 
-function initializeRepository(): string {
-  const root = temporaryDirectory("ascout-t107-repo-");
+function initializeRepository(root = temporaryDirectory("ascout-t107-repo-")): string {
   git(root, ["init", "-q"]);
   git(root, ["config", "user.name", "Ascout T107"]);
   git(root, ["config", "user.email", "t107@example.invalid"]);
@@ -71,8 +70,8 @@ interface SimpleRepository {
   readonly headTree: string;
 }
 
-function createSimpleRepository(): SimpleRepository {
-  const root = initializeRepository();
+function buildSimpleRepository(root?: string): SimpleRepository {
+  root = initializeRepository(root);
   writeFileSync(join(root, "tracked.txt"), "base\n", "utf8");
   const base = commitAll(root, "base");
   writeFileSync(join(root, "tracked.txt"), "head\n", "utf8");
@@ -80,6 +79,18 @@ function createSimpleRepository(): SimpleRepository {
   return { root, base, head, headTree: git(root, ["rev-parse", `${head}^{tree}`]) };
 }
 
+// Build the two-commit fixture once per file and give every caller a private
+// copy. Each build costs about 12 Git processes, which dominated these tests on
+// hosted Windows (#601). Copies keep per-test isolation and identical history.
+let simpleTemplate: SimpleRepository | undefined;
+
+function createSimpleRepository(): SimpleRepository {
+  simpleTemplate ??= buildSimpleRepository(mkdtempSync(join(tmpdir(), "ascout-t107-template-")));
+  const root = temporaryDirectory("ascout-t107-repo-");
+  cpSync(simpleTemplate.root, root, { recursive: true });
+  return { ...simpleTemplate, root };
+}
+
 function writeRuntimeFile(root: string, relativePath: string, content: string): void {
   const path = join(root, relativePath);
   mkdirSync(dirname(path), { recursive: true });
@@ -335,6 +346,10 @@ function expectNoEvidence(outputDir: string): void {
   for (const file of EVIDENCE_FILES) expect(existsSync(join(outputDir, file))).toBe(false);
 }
 
+afterAll(() => {
+  if (simpleTemplate) rmSync(simpleTemplate.root, { recursive: true, force: true });
+});
+
 afterEach(() => {
   while (temporaryPaths.length > 0) {
     const path = temporaryPaths.pop();
```

## Full file at head: tests/t107-self-verification-harness.contract.test.ts
```
    1| import { execFileSync } from "node:child_process";
    2| import { cpSync, existsSync, mkdirSync, mkdtempSync, promises as fsPromises, readFileSync, renameSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
    3| import { tmpdir } from "node:os";
    4| import { dirname, join } from "node:path";
    5| 
    6| import { afterAll, afterEach, describe, expect, it } from "vitest";
    7| 
    8| import {
    9|   SelfVerificationIntegrityError,
   10|   buildQualificationEnvelope,
   11|   prepareExactHeadRuntime,
   12|   reconstructSelfVerificationSubject,
   13|   releaseExactHeadRuntime,
   14|   requireUniqueMergeBaseOutput,
   15|   runSelfVerification,
   16|   validateReceiptCapture,
   17|   verifyExactHeadRuntimeManifest,
   18| } from "../benchmarks/self-verify.mjs";
   19| import { composeSourceState } from "../src/check.js";
   20| import { validateReceiptJsonSchema } from "../src/receipt/json.js";
   21| import {
   22|   decideReceiptExitCode,
   23|   deriveReceiptCompleteness,
   24|   validateReceiptSemantics,
   25|   type ReceiptExitCode,
   26|   type ReceiptV1,
   27|   type SourceStateV1,
   28|   type TaskResultV1,
   29| } from "../src/receipt/model.js";
   30| 
   31| const temporaryPaths: string[] = [];
   32| const EVIDENCE_FILES = ["self-verification-receipt.json", "self-verification-envelope.json"] as const;
   33| const RECEIPT_SCHEMA_PATH = join("specs", "001-changed-code-verification-receipt", "contracts", "receipt-v1.schema.json");
   34| 
   35| function temporaryDirectory(prefix: string): string {
   36|   const path = mkdtempSync(join(tmpdir(), prefix));
   37|   temporaryPaths.push(path);
   38|   return path;
   39| }
   40| 
   41| function temporaryOutputPath(prefix: string): string {
   42|   return join(temporaryDirectory(prefix), "evidence");
   43| }
   44| 
   45| function git(root: string, args: readonly string[]): string {
   46|   return execFileSync("git", ["-C", root, ...args], {
   47|     encoding: "utf8",
   48|     stdio: ["ignore", "pipe", "pipe"],
   49|   }).trim();
   50| }
   51| 
   52| function initializeRepository(root = temporaryDirectory("ascout-t107-repo-")): string {
   53|   git(root, ["init", "-q"]);
   54|   git(root, ["config", "user.name", "Ascout T107"]);
   55|   git(root, ["config", "user.email", "t107@example.invalid"]);
   56|   writeFileSync(join(root, ".gitignore"), "dist/\nnode_modules/\ncoverage/\n.ascout/\n", "utf8");
   57|   return root;
   58| }
   59| 
   60| function commitAll(root: string, message: string): string {
   61|   git(root, ["add", "-A"]);
   62|   git(root, ["commit", "-q", "-m", message]);
   63|   return git(root, ["rev-parse", "HEAD"]);
   64| }
   65| 
   66| interface SimpleRepository {
   67|   readonly root: string;
   68|   readonly base: string;
   69|   readonly head: string;
   70|   readonly headTree: string;
   71| }
   72| 
   73| function buildSimpleRepository(root?: string): SimpleRepository {
   74|   root = initializeRepository(root);
   75|   writeFileSync(join(root, "tracked.txt"), "base\n", "utf8");
   76|   const base = commitAll(root, "base");
   77|   writeFileSync(join(root, "tracked.txt"), "head\n", "utf8");
   78|   const head = commitAll(root, "head");
   79|   return { root, base, head, headTree: git(root, ["rev-parse", `${head}^{tree}`]) };
   80| }
   81| 
   82| // Build the two-commit fixture once per file and give every caller a private
   83| // copy. Each build costs about 12 Git processes, which dominated these tests on
   84| // hosted Windows (#601). Copies keep per-test isolation and identical history.
   85| let simpleTemplate: SimpleRepository | undefined;
   86| 
   87| function createSimpleRepository(): SimpleRepository {
   88|   simpleTemplate ??= buildSimpleRepository(mkdtempSync(join(tmpdir(), "ascout-t107-template-")));
   89|   const root = temporaryDirectory("ascout-t107-repo-");
   90|   cpSync(simpleTemplate.root, root, { recursive: true });
   91|   return { ...simpleTemplate, root };
   92| }
   93| 
   94| function writeRuntimeFile(root: string, relativePath: string, content: string): void {
   95|   const path = join(root, relativePath);
   96|   mkdirSync(dirname(path), { recursive: true });
   97|   writeFileSync(path, content, "utf8");
   98| }
   99| 
  100| function createBuildableFixture({ contaminateTracked = false, createRuntimeSymlink = false } = {}): SimpleRepository {
  101|   const root = initializeRepository();
  102|   writeFileSync(join(root, "tracked.txt"), "base\n", "utf8");
  103|   const base = commitAll(root, "base");
  104|   writeFileSync(join(root, "tracked.txt"), "head\n", "utf8");
  105|   writeFileSync(join(root, "package.json"), JSON.stringify({
  106|     name: "ascout-t107-runtime-fixture",
  107|     version: "1.0.0",
  108|     private: true,
  109|     type: "module",
  110|     scripts: { build: "node build.mjs" },
  111|   }, null, 2) + "\n", "utf8");
  112|   writeFileSync(join(root, "package-lock.json"), JSON.stringify({
  113|     name: "ascout-t107-runtime-fixture",
  114|     version: "1.0.0",
  115|     lockfileVersion: 3,
  116|     requires: true,
  117|     packages: { "": { name: "ascout-t107-runtime-fixture", version: "1.0.0" } },
  118|   }, null, 2) + "\n", "utf8");
  119|   writeRuntimeFile(root, RECEIPT_SCHEMA_PATH, "{\"fixture\":true}\n");
  120|   writeFileSync(join(root, "build.mjs"), [
  121|     'import { mkdirSync, symlinkSync, writeFileSync } from "node:fs";',
  122|     'import { dirname, join } from "node:path";',
  123|     'const files = {',
  124|     '  "cli.js": "export const fixtureCli = 1;\\n",',
  125|     '  "check.js": "export const fixtureCheck = 1;\\n",',
  126|     '  "receipt/json.js": "export const fixtureJson = 1;\\n",',
  127|     '  "receipt/model.js": "export const fixtureModel = 1;\\n",',
  128|     '  "nested/runtime.js": "export const fixtureNested = 1;\\n",',
  129|     '};',
  130|     'for (const [name, value] of Object.entries(files)) {',
  131|     '  const target = join(process.cwd(), "dist", name);',
  132|     '  mkdirSync(dirname(target), { recursive: true });',
  133|     '  writeFileSync(target, value, "utf8");',
  134|     '}',
  135|     ...(createRuntimeSymlink ? [
  136|       'mkdirSync(join(process.cwd(), "node_modules", "linked-runtime"), { recursive: true });',
  137|       'writeFileSync(join(process.cwd(), "node_modules", "linked-runtime", "target.js"), "export const linked = 1;\\n", "utf8");',
  138|       'symlinkSync(join("linked-runtime", "target.js"), join(process.cwd(), "node_modules", "linked-target.js"));',
  139|     ] : []),
  140|     ...(contaminateTracked ? ['writeFileSync(join(process.cwd(), "tracked.txt"), "contaminated\\n", "utf8");'] : []),
  141|   ].join("\n") + "\n", "utf8");
  142|   const head = commitAll(root, "head with exact build contract");
  143|   return { root, base, head, headTree: git(root, ["rev-parse", `${head}^{tree}`]) };
  144| }
  145| 
  146| function baselineTask(): TaskResultV1 {
  147|   return {
  148|     task_id: "lint-t107",
  149|     task_type: "lint",
  150|     authorized_by: "discovery",
  151|     source_path: null,
  152|     argv: ["eslint", "tracked.txt"],
  153|     argv_redacted: false,
  154|     tool_name: "eslint",
  155|     tool_version: "1.0.0",
  156|     command_surface_changed: false,
  157|     changed_authority_paths: [],
  158|     execution_admission: "normal",
  159|     status: "PASS",
  160|     reason_code: null,
  161|     reason_text: null,
  162|     exit_code: 0,
  163|     started_at: "2026-09-03T17:00:00.000Z",
  164|     finished_at: "2026-09-03T17:00:01.000Z",
  165|     duration_ms: 1000,
  166|     observations: { runs: 1, failures: 0 },
  167|     cache_state: "cold",
  168|     evidence_ids: [],
  169|     artifact_refs: [],
  170|     output_truncated: false,
  171|   };
  172| }
  173| 
  174| function taskForExit(exitCode: ReceiptExitCode): TaskResultV1 {
  175|   const task = baselineTask();
  176|   if (exitCode === 0 || exitCode === 3) return task;
  177|   if (exitCode === 1) return { ...task, status: "FAIL", exit_code: 1, observations: { runs: 1, failures: 1 } };
  178|   if (exitCode === 2) {
  179|     return {
  180|       ...task,
  181|       status: "ERROR",
  182|       reason_code: "execution_error",
  183|       reason_text: "The fixture intentionally models an internal execution error.",
  184|       exit_code: 2,
  185|       observations: { runs: 0, failures: 0 },
  186|     };
  187|   }
  188|   return {
  189|     ...task,
  190|     argv: [],
  191|     tool_name: null,
  192|     tool_version: null,
  193|     status: "BLOCKED",
  194|     reason_code: "prerequisite_blocked",
  195|     reason_text: "The fixture intentionally models material incompleteness.",
  196|     exit_code: null,
  197|     started_at: null,
  198|     finished_at: null,
  199|     duration_ms: null,
  200|     observations: { runs: 0, failures: 0 },
  201|     cache_state: "not_applicable",
  202|   };
  203| }
  204| 
  205| function synchronizeSummary(receipt: ReceiptV1): void {
  206|   const counts = { PASS: 0, FAIL: 0, FLAKY: 0, BLOCKED: 0, ERROR: 0, NOT_APPLICABLE: 0, NOT_RUN: 0 };
  207|   for (const task of receipt.tasks) counts[task.status] += 1;
  208|   (receipt.summary as unknown as { task_status_counts: typeof counts }).task_status_counts = counts;
  209|   (receipt.summary as unknown as { completeness: ReceiptV1["summary"]["completeness"] }).completeness = deriveReceiptCompleteness(receipt);
  210|   (receipt.summary as unknown as { exit_code: ReceiptExitCode }).exit_code = decideReceiptExitCode(receipt);
  211| }
  212| 
  213| function validReceipt(source: SourceStateV1, desiredExit: ReceiptExitCode): ReceiptV1 {
  214|   const task = taskForExit(desiredExit);
  215|   const endSource: SourceStateV1 = desiredExit === 3 ? { ...source, tree_digest: "f".repeat(64) } : { ...source };
  216|   const receipt: ReceiptV1 = {
  217|     schema_version: "1.0",
  218|     run: {
  219|       run_id: "run-t107",
  220|       ascout_version: "0.0.0",
  221|       started_at: "2026-09-03T17:00:00.000Z",
  222|       finished_at: "2026-09-03T17:00:01.000Z",
  223|       config_digest: "d".repeat(64),
  224|     },
  225|     source: { start: { ...source }, end: endSource },
  226|     comparison: {
  227|       kind: "working_tree_vs_head",
  228|       base_ref: source.head_sha,
  229|       includes_staged: true,
  230|       includes_unstaged: true,
  231|       includes_untracked_nonignored: true,
  232|       changed_files: [{
  233|         path: "tracked.txt",
  234|         change_kind: "modified",
  235|         line_semantics: "text",
  236|         changed_new_line_ranges: [[1, 1]],
  237|         is_test_file: false,
  238|         is_snapshot: false,
  239|         is_command_surface: false,
  240|       }],
  241|     },
  242|     selection: {
  243|       mode: "no_test_task",
  244|       initial_scope: { kind: "repository", path: null },
  245|       selected_test_count: null,
  246|       deselected_test_count: null,
  247|       total_test_count: null,
  248|       widened: false,
  249|       widen_triggers: [],
  250|       passes: [],
  251|       limitations: ["T107 receipt fixture has no test task"],
  252|     },
  253|     tasks: [task],
  254|     changed_code: { changed_file_count: 1, changed_text_line_count: 1 },
  255|     exercise: {
  256|       changed_executable_lines: 0,
  257|       exercised_lines: 0,
  258|       not_exercised_lines: 0,
  259|       unresolved_lines: 0,
  260|       changed_files_with_zero_exercised_lines: 0,
  261|       records: [],
  262|     },
  263|     test_changes: [],
  264|     findings: [],
  265|     evidence: [],
  266|     artifacts: [],
  267|     stability: desiredExit === 3 ? "tree_drifted" : "stable",
  268|     summary: {
  269|       task_status_counts: { PASS: 0, FAIL: 0, FLAKY: 0, BLOCKED: 0, ERROR: 0, NOT_APPLICABLE: 0, NOT_RUN: 0 },
  270|       finding_count: 0,
  271|       completeness: "complete",
  272|       exit_code: 0,
  273|     },
  274|   };
  275|   synchronizeSummary(receipt);
  276|   expect(receipt.summary.exit_code).toBe(desiredExit);
  277|   return receipt;
  278| }
  279| 
  280| function validators() {
  281|   return { validateReceiptJsonSchema, validateReceiptSemantics };
  282| }
  283| 
  284| function runtimeFor(exitCode: ReceiptExitCode, mutate?: (receipt: ReceiptV1) => void, argvSink?: string[][]) {
  285|   return {
  286|     composeSourceState,
  287|     validateReceiptJsonSchema,
  288|     validateReceiptSemantics,
  289|     runVerifier: async ({ repositoryRoot, argv }: { repositoryRoot: string; argv: string[] }) => {
  290|       argvSink?.push([...argv]);
  291|       const receipt = validReceipt(composeSourceState(repositoryRoot), exitCode);
  292|       mutate?.(receipt);
  293|       return {
  294|         outcome: "exited",
  295|         exitCode,
  296|         signal: null,
  297|         error: null,
  298|         stdout: Buffer.from(JSON.stringify(receipt), "utf8"),
  299|         stderr: Buffer.alloc(0),
  300|         stdoutTruncated: false,
  301|         stderrTruncated: false,
  302|       };
  303|     },
  304|   };
  305| }
  306| 
  307| function runtimeWithExecution(execution: Record<string, unknown>) {
  308|   return {
  309|     composeSourceState,
  310|     validateReceiptJsonSchema,
  311|     validateReceiptSemantics,
  312|     runVerifier: async () => ({
  313|       outcome: "exited",
  314|       exitCode: 0,
  315|       signal: null,
  316|       error: null,
  317|       stdout: Buffer.alloc(0),
  318|       stderr: Buffer.alloc(0),
  319|       stdoutTruncated: false,
  320|       stderrTruncated: false,
  321|       ...execution,
  322|     }),
  323|   };
  324| }
  325| 
  326| async function capture(simple: SimpleRepository, exitCode: ReceiptExitCode, mutate?: (receipt: ReceiptV1) => void, argvSink?: string[][]) {
  327|   git(simple.root, ["reset", "--hard", simple.head]);
  328|   git(simple.root, ["clean", "-fd"]);
  329|   const outputDir = temporaryOutputPath("ascout-t107-output-");
  330|   return await runSelfVerification({
  331|     repositoryRoot: simple.root,
  332|     eventBaseSha: simple.base,
  333|     headSha: simple.head,
  334|     outputDir,
  335|     testRuntime: runtimeFor(exitCode, mutate, argvSink),
  336|   });
  337| }
  338| 
  339| function expectIntegrityCode(error: unknown, code: string): boolean {
  340|   expect(error).toBeInstanceOf(SelfVerificationIntegrityError);
  341|   expect((error as SelfVerificationIntegrityError).code).toBe(code);
  342|   return true;
  343| }
  344| 
  345| function expectNoEvidence(outputDir: string): void {
  346|   for (const file of EVIDENCE_FILES) expect(existsSync(join(outputDir, file))).toBe(false);
  347| }
  348| 
  349| afterAll(() => {
  350|   if (simpleTemplate) rmSync(simpleTemplate.root, { recursive: true, force: true });
  351| });
  352| 
  353| afterEach(() => {
  354|   while (temporaryPaths.length > 0) {
  355|     const path = temporaryPaths.pop();
  356|     if (path) rmSync(path, { recursive: true, force: true });
  357|   }
  358| });
  359| 
  360| describe("T107 exact-tree self-verification harness", () => {
  361|   it("requires exact H and reconstructs B == M", async () => {
  362|     const simple = createSimpleRepository();
  363|     const result = await reconstructSelfVerificationSubject({ repositoryRoot: simple.root, eventBaseSha: simple.base, headSha: simple.head });
  364|     expect(result).toEqual({ eventBaseSha: simple.base, headSha: simple.head, mergeBaseSha: simple.base, headTreeSha: simple.headTree });
  365|     expect(git(simple.root, ["rev-parse", "HEAD"])).toBe(simple.base);
  366|     expect(git(simple.root, ["write-tree"])).toBe(simple.headTree);
  367|   }, 15_000);
  368| 
  369|   it("rejects wrong H, unavailable B, and absent or multiple merge bases", async () => {
  370|     const simple = createSimpleRepository();
  371|     await expect(reconstructSelfVerificationSubject({ repositoryRoot: simple.root, eventBaseSha: simple.base, headSha: simple.base }))
  372|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "head_mismatch"));
  373|     git(simple.root, ["reset", "--hard", simple.head]);
  374|     await expect(reconstructSelfVerificationSubject({ repositoryRoot: simple.root, eventBaseSha: "f".repeat(40), headSha: simple.head }))
  375|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "git_identity_unavailable"));
  376|     expect(() => requireUniqueMergeBaseOutput("")).toThrowError(SelfVerificationIntegrityError);
  377|     expect(() => requireUniqueMergeBaseOutput(`${"a".repeat(40)}\n${"b".repeat(40)}\n`)).toThrowError(SelfVerificationIntegrityError);
  378|     expect(requireUniqueMergeBaseOutput(`${"c".repeat(40)}\n`)).toBe("c".repeat(40));
  379|   }, 15_000);
  380| 
  381|   it("uses unique M when event base E advanced independently", async () => {
  382|     const root = initializeRepository();
  383|     writeFileSync(join(root, "tracked.txt"), "merge-base\n", "utf8");
  384|     const mergeBase = commitAll(root, "merge base");
  385|     git(root, ["branch", "feature", mergeBase]);
  386|     git(root, ["checkout", "-q", "feature"]);
  387|     writeFileSync(join(root, "tracked.txt"), "feature\n", "utf8");
  388|     const head = commitAll(root, "feature head");
  389|     const headTree = git(root, ["rev-parse", `${head}^{tree}`]);
  390|     git(root, ["checkout", "-q", "master"]);
  391|     writeFileSync(join(root, "base-only.txt"), "advanced base\n", "utf8");
  392|     const eventBase = commitAll(root, "advanced base");
  393|     git(root, ["checkout", "-q", "--detach", head]);
  394|     const result = await reconstructSelfVerificationSubject({ repositoryRoot: root, eventBaseSha: eventBase, headSha: head });
  395|     expect(eventBase).not.toBe(mergeBase);
  396|     expect(result.mergeBaseSha).toBe(mergeBase);
  397|     expect(git(root, ["rev-parse", "HEAD"])).toBe(mergeBase);
  398|     expect(git(root, ["write-tree"])).toBe(headTree);
  399|   }, 15_000);
  400| 
  401|   it("preserves added, deleted, renamed, and modified tracked content as exact H tree", async () => {
  402|     const root = initializeRepository();
  403|     writeFileSync(join(root, "modified.txt"), "base\n", "utf8");
  404|     writeFileSync(join(root, "deleted.txt"), "delete me\n", "utf8");
  405|     writeFileSync(join(root, "rename-old.txt"), "rename me\n", "utf8");
  406|     const base = commitAll(root, "base shapes");
  407|     writeFileSync(join(root, "modified.txt"), "head\n", "utf8");
  408|     rmSync(join(root, "deleted.txt"));
  409|     renameSync(join(root, "rename-old.txt"), join(root, "rename-new.txt"));
  410|     writeFileSync(join(root, "added.txt"), "new\n", "utf8");
  411|     const head = commitAll(root, "head shapes");
  412|     const headTree = git(root, ["rev-parse", `${head}^{tree}`]);
  413|     await reconstructSelfVerificationSubject({ repositoryRoot: root, eventBaseSha: base, headSha: head });
  414|     expect(git(root, ["write-tree"])).toBe(headTree);
  415|     const staged = git(root, ["diff", "--cached", "--name-status", "--find-renames", base]);
  416|     for (const path of ["added.txt", "deleted.txt", "modified.txt", "rename-new.txt"]) expect(staged).toContain(path);
  417|   });
  418| 
  419|   it("fails closed for tracked/untracked contamination while allowing canonical ignored paths", async () => {
  420|     const tracked = createSimpleRepository();
  421|     writeFileSync(join(tracked.root, "tracked.txt"), "drift\n", "utf8");
  422|     await expect(reconstructSelfVerificationSubject({ repositoryRoot: tracked.root, eventBaseSha: tracked.base, headSha: tracked.head }))
  423|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "tracked_contamination"));
  424| 
  425|     const untracked = createSimpleRepository();
  426|     writeFileSync(join(untracked.root, "rogue.txt"), "rogue\n", "utf8");
  427|     await expect(reconstructSelfVerificationSubject({ repositoryRoot: untracked.root, eventBaseSha: untracked.base, headSha: untracked.head }))
  428|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "untracked_contamination"));
  429| 
  430|     const ignored = createSimpleRepository();
  431|     for (const path of [join("dist", "ignored.js"), join("node_modules", "fixture", "ignored.js"), join(".ascout", "ignored.txt")]) {
  432|       writeRuntimeFile(ignored.root, path, "ignored\n");
  433|     }
  434|     await expect(reconstructSelfVerificationSubject({ repositoryRoot: ignored.root, eventBaseSha: ignored.base, headSha: ignored.head }))
  435|       .resolves.toMatchObject({ mergeBaseSha: ignored.base });
  436|   }, 15_000);
  437| 
  438|   it("provisions a private exact-H runtime from a clean exact-lockfile install and ignores subject dist/node_modules", async () => {
  439|     const fixture = createBuildableFixture();
  440|     writeRuntimeFile(fixture.root, join("node_modules", "typescript", "bin", "tsc"), "throw new Error('subject compiler must not run');\n");
  441|     writeRuntimeFile(fixture.root, join("dist", "check.js"), "export const poisoned = true;\n");
  442| 
  443|     const prepared = await prepareExactHeadRuntime(fixture.root, fixture.head, { requireExistingHeadBuild: false });
  444|     try {
  445|       expect(prepared.repositoryRoot).not.toBe(fixture.root);
  446|       expect(prepared.headSha).toBe(fixture.head);
  447|       expect(prepared.headTreeSha).toBe(fixture.headTree);
  448|       expect(readFileSync(join(prepared.runtimeRoot, "check.js"), "utf8")).toBe("export const fixtureCheck = 1;\n");
  449|       writeRuntimeFile(fixture.root, join("dist", "check.js"), "export const changedAgain = true;\n");
  450|       expect(readFileSync(join(prepared.runtimeRoot, "check.js"), "utf8")).toBe("export const fixtureCheck = 1;\n");
  451|     } finally {
  452|       await releaseExactHeadRuntime(fixture.root, prepared);
  453|     }
  454|   }, 15_000);
  455| 
  456|   it("binds schema and installed dependency-tree assets against post-build tampering", async () => {
  457|     const fixture = createBuildableFixture();
  458|     const prepared = await prepareExactHeadRuntime(fixture.root, fixture.head, { requireExistingHeadBuild: false });
  459|     try {
  460|       await expect(verifyExactHeadRuntimeManifest(prepared)).resolves.toBeUndefined();
  461|       const schemaPath = join(prepared.repositoryRoot, RECEIPT_SCHEMA_PATH);
  462|       const schemaBytes = readFileSync(schemaPath, "utf8");
  463|       writeFileSync(schemaPath, "{\"tampered\":true}\n", "utf8");
  464|       await expect(verifyExactHeadRuntimeManifest(prepared))
  465|         .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "runtime_provenance_mismatch"));
  466| 
  467|       writeFileSync(schemaPath, schemaBytes, "utf8");
  468|       await expect(verifyExactHeadRuntimeManifest(prepared)).resolves.toBeUndefined();
  469|       writeRuntimeFile(prepared.repositoryRoot, join("node_modules", "injected", "runtime.js"), "export const tampered = true;\n");
  470|       await expect(verifyExactHeadRuntimeManifest(prepared))
  471|         .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "runtime_provenance_mismatch"));
  472|     } finally {
  473|       await releaseExactHeadRuntime(fixture.root, prepared);
  474|     }
  475|   }, 15_000);
  476| 
  477|   it.skipIf(process.platform === "win32")("binds resolved bytes behind private runtime symlinks", async () => {
  478|     const fixture = createBuildableFixture({ createRuntimeSymlink: true });
  479|     const prepared = await prepareExactHeadRuntime(fixture.root, fixture.head, { requireExistingHeadBuild: false });
  480|     try {
  481|       await expect(verifyExactHeadRuntimeManifest(prepared)).resolves.toBeUndefined();
  482|       writeFileSync(join(prepared.repositoryRoot, "node_modules", "linked-runtime", "target.js"), "export const linked = 2;\n", "utf8");
  483|       await expect(verifyExactHeadRuntimeManifest(prepared))
  484|         .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "runtime_provenance_mismatch"));
  485|     } finally {
  486|       await releaseExactHeadRuntime(fixture.root, prepared);
  487|     }
  488|   });
  489| 
  490|   it("rejects an isolated exact-H build that contaminates tracked source", async () => {
  491|     const fixture = createBuildableFixture({ contaminateTracked: true });
  492|     await expect(prepareExactHeadRuntime(fixture.root, fixture.head, { requireExistingHeadBuild: false }))
  493|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "tracked_contamination"));
  494|   }, 15_000);
  495| 
  496|   it.each([0, 1, 3, 4] as const)("retains valid source-bound exit %s as SHADOW_NON_GATING evidence", async (exitCode) => {
  497|     const result = await capture(createSimpleRepository(), exitCode);
  498|     expect(result.receiptExit).toBe(exitCode);
  499|     expect(result.envelope.classification).toBe("SHADOW_NON_GATING");
  500|     expect(result.envelope.receipt_exit_code).toBe(exitCode);
  501|     expect(existsSync(result.receiptPath)).toBe(true);
  502|     expect(existsSync(result.envelopePath)).toBe(true);
  503|   }, 15_000);
  504| 
  505|   it("rejects otherwise-valid source-bound exit 2 before digest/envelope/output", async () => {
  506|     const simple = createSimpleRepository();
  507|     const outputDir = temporaryOutputPath("ascout-t107-exit2-");
  508|     await expect(runSelfVerification({ repositoryRoot: simple.root, eventBaseSha: simple.base, headSha: simple.head, outputDir, testRuntime: runtimeFor(2) }))
  509|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "exit_2_integrity_failure"));
  510|     expectNoEvidence(outputDir);
  511|     expect(existsSync(outputDir)).toBe(false);
  512|   }, 15_000);
  513| 
  514|   it("rejects process mismatch, malformed JSON, schema invalidity, semantic invalidity, and missing receipt", () => {
  515|     const source = {
  516|       repository_id: `local:${"a".repeat(64)}`,
  517|       repository_id_kind: "local_only" as const,
  518|       portable: false,
  519|       head_sha: "b".repeat(40),
  520|       detached: true,
  521|       shallow: false,
  522|       tree_digest_version: 1 as const,
  523|       tree_digest: "c".repeat(64),
  524|       tracked_index_entry_count: 1,
  525|       unstaged_changed_count: 0,
  526|       included_untracked_count: 0,
  527|     } satisfies SourceStateV1;
  528|     const receipt = validReceipt(source, 0);
  529|     const bytes = Buffer.from(JSON.stringify(receipt));
  530| 
  531|     expect(() => validateReceiptCapture({ receiptBytes: bytes, processExitCode: 1, expectedSourceState: source, validators: validators() })).toThrowError(/process exit/u);
  532|     expect(() => validateReceiptCapture({ receiptBytes: Buffer.from("not json"), processExitCode: 0, expectedSourceState: source, validators: validators() })).toThrowError(/valid JSON/u);
  533| 
  534|     const schemaInvalid = structuredClone(receipt) as unknown as Record<string, unknown>;
  535|     schemaInvalid.schema_version = "9.0";
  536|     expect(() => validateReceiptCapture({ receiptBytes: Buffer.from(JSON.stringify(schemaInvalid)), processExitCode: 0, expectedSourceState: source, validators: validators() })).toThrowError(/JSON Schema/u);
  537| 
  538|     const semanticInvalid = structuredClone(receipt);
  539|     (semanticInvalid.summary as unknown as { finding_count: number }).finding_count = 1;
  540|     expect(validateReceiptJsonSchema(semanticInvalid).valid).toBe(true);
  541|     expect(validateReceiptSemantics(semanticInvalid).valid).toBe(false);
  542|     expect(() => validateReceiptCapture({ receiptBytes: Buffer.from(JSON.stringify(semanticInvalid)), processExitCode: 0, expectedSourceState: source, validators: validators() })).toThrowError(/semantic validator/u);
  543|     expect(() => validateReceiptCapture({ receiptBytes: Buffer.alloc(0), processExitCode: 2, expectedSourceState: source, validators: validators() })).toThrowError(/no receipt bytes/u);
  544|   });
  545| 
  546|   it("rejects each of the six canonical source-binding fields independently", () => {
  547|     const source = {
  548|       repository_id: `local:${"a".repeat(64)}`,
  549|       repository_id_kind: "local_only" as const,
  550|       portable: false,
  551|       head_sha: "b".repeat(40),
  552|       detached: true,
  553|       shallow: false,
  554|       tree_digest_version: 1 as const,
  555|       tree_digest: "c".repeat(64),
  556|       tracked_index_entry_count: 3,
  557|       unstaged_changed_count: 0,
  558|       included_untracked_count: 0,
  559|     } satisfies SourceStateV1;
  560|     const passThroughValidators = {
  561|       validateReceiptJsonSchema: () => ({ valid: true, issues: [] }),
  562|       validateReceiptSemantics: () => ({ valid: true, issues: [] }),
  563|     };
  564|     const mutations: Record<string, (candidate: Record<string, unknown>) => void> = {
  565|       head_sha: (candidate) => { candidate.head_sha = "d".repeat(40); },
  566|       tree_digest_version: (candidate) => { candidate.tree_digest_version = 2; },
  567|       tree_digest: (candidate) => { candidate.tree_digest = "e".repeat(64); },
  568|       tracked_index_entry_count: (candidate) => { candidate.tracked_index_entry_count = 4; },
  569|       unstaged_changed_count: (candidate) => { candidate.unstaged_changed_count = 1; },
  570|       included_untracked_count: (candidate) => { candidate.included_untracked_count = 1; },
  571|     };
  572|     for (const [field, mutate] of Object.entries(mutations)) {
  573|       const receipt = validReceipt(source, 0);
  574|       mutate(receipt.source.start as unknown as Record<string, unknown>);
  575|       expect(() => validateReceiptCapture({ receiptBytes: Buffer.from(JSON.stringify(receipt)), processExitCode: 0, expectedSourceState: source, validators: passThroughValidators }), field)
  576|         .toThrowError(new RegExp(field, "u"));
  577|     }
  578|   });
  579| 
  580|   it("hashes exact retained bytes, keeps envelope allowlisted, and never adds command admission", async () => {
  581|     const simple = createSimpleRepository();
  582|     const argv: string[][] = [];
  583|     const result = await capture(simple, 0, undefined, argv);
  584|     const bytes = readFileSync(result.receiptPath);
  585|     const crypto = await import("node:crypto");
  586|     expect(result.receiptSha256).toBe(crypto.createHash("sha256").update(bytes).digest("hex"));
  587|     expect(Object.keys(result.envelope)).toEqual([
  588|       "schema_version",
  589|       "classification",
  590|       "verifier_head_sha",
  591|       "verifier_head_tree_sha",
  592|       "event_base_tip_sha",
  593|       "subject_merge_base_sha",
  594|       "subject_target_head_sha",
  595|       "subject_target_tree_sha",
  596|       "receipt_exit_code",
  597|       "receipt_sha256",
  598|       "receipt_file",
  599|     ]);
  600|     expect(JSON.stringify(result.envelope)).not.toMatch(/repository_url|absolute|actor|hostname|home|token|secret|stderr|stdout/ui);
  601|     expect(argv).toHaveLength(1);
  602|     expect(argv[0]).toContain("check");
  603|     expect(argv[0]).toContain("--format");
  604|     expect(argv[0]).toContain("json");
  605|     expect(argv[0]).not.toContain("--allow-changed-command-surface");
  606|   }, 15_000);
  607| 
  608|   it("keeps focused tests independent of pre-existing dist but production fails closed when the supplied head build is missing", async () => {
  609|     const focused = createSimpleRepository();
  610|     expect(existsSync(join(focused.root, "dist"))).toBe(false);
  611|     await expect(capture(focused, 0)).resolves.toMatchObject({ receiptExit: 0 });
  612|     expect(existsSync(join(focused.root, "dist"))).toBe(false);
  613| 
  614|     const production = createSimpleRepository();
  615|     const outputDir = temporaryOutputPath("ascout-t107-production-missing-");
  616|     await expect(runSelfVerification({ repositoryRoot: production.root, eventBaseSha: production.base, headSha: production.head, outputDir }))
  617|       .rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "head_build_unavailable"));
  618|     expectNoEvidence(outputDir);
  619|     expect(existsSync(outputDir)).toBe(false);
  620|   }, 15_000);
  621| 
  622|   it.each([
  623|     ["timed_out", { outcome: "timed_out", exitCode: null, signal: null, error: null }, "verifier_execution_failed"],
  624|     ["spawn error", { outcome: "error", exitCode: null, signal: null, error: new Error("fixture") }, "verifier_execution_failed"],
  625|     ["stdout truncated", { outcome: "exited", exitCode: 0, stdoutTruncated: true }, "verifier_output_truncated"],
  626|     ["stderr truncated", { outcome: "exited", exitCode: 0, stderrTruncated: true }, "verifier_output_truncated"],
  627|   ] as const)("fails closed for %s without writing evidence", async (_label, execution, expectedCode) => {
  628|     const simple = createSimpleRepository();
  629|     const outputDir = temporaryOutputPath("ascout-t107-execution-failure-");
  630|     await expect(runSelfVerification({
  631|       repositoryRoot: simple.root,
  632|       eventBaseSha: simple.base,
  633|       headSha: simple.head,
  634|       outputDir,
  635|       testRuntime: runtimeWithExecution(execution as unknown as Record<string, unknown>),
  636|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, expectedCode));
  637|     expectNoEvidence(outputDir);
  638|     expect(existsSync(outputDir)).toBe(false);
  639|   }, 15_000);
  640| 
  641|   it.skipIf(process.platform === "win32")("rejects output-path replacement with a repository symlink without repository evidence", async () => {
  642|     const simple = createSimpleRepository();
  643|     const outputDir = temporaryOutputPath("ascout-t107-output-race-");
  644|     const repositoryTarget = join(simple.root, "evidence-target");
  645|     mkdirSync(repositoryTarget);
  646|     const baseRuntime = runtimeFor(0);
  647|     const replacingRuntime = {
  648|       ...baseRuntime,
  649|       runVerifier: async (args: { repositoryRoot: string; argv: string[] }) => {
  650|         const result = await baseRuntime.runVerifier(args);
  651|         symlinkSync(repositoryTarget, outputDir, "dir");
  652|         return result;
  653|       },
  654|     };
  655| 
  656|     await expect(runSelfVerification({
  657|       repositoryRoot: simple.root,
  658|       eventBaseSha: simple.base,
  659|       headSha: simple.head,
  660|       outputDir,
  661|       testRuntime: replacingRuntime,
  662|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_exists"));
  663|     expectNoEvidence(repositoryTarget);
  664|   });
  665| 
  666|   it.skipIf(process.platform === "win32")("rejects output parent replacement before bound publication without repository evidence", async () => {
  667|     const simple = createSimpleRepository();
  668|     const outputDir = temporaryOutputPath("ascout-t107-parent-race-");
  669|     const outputParent = dirname(outputDir);
  670|     const displacedParent = `${outputParent}-displaced`;
  671|     const repositoryTarget = join(simple.root, "parent-target");
  672|     mkdirSync(repositoryTarget);
  673|     temporaryPaths.push(displacedParent);
  674|     let replaced = false;
  675| 
  676|     await expect(runSelfVerification({
  677|       repositoryRoot: simple.root,
  678|       eventBaseSha: simple.base,
  679|       headSha: simple.head,
  680|       outputDir,
  681|       testRuntime: runtimeFor(0),
  682|       testEvidenceIo: {
  683|         beforeBoundParentPublish: async () => {
  684|           renameSync(outputParent, displacedParent);
  685|           symlinkSync(repositoryTarget, outputParent, "dir");
  686|           replaced = true;
  687|         },
  688|       },
  689|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  690|     expect(replaced).toBe(true);
  691|     expectNoEvidence(repositoryTarget);
  692|     expectNoEvidence(join(displacedParent, "evidence"));
  693|     expectNoEvidence(outputDir);
  694|   });
  695| 
  696|   it.skipIf(process.platform === "win32")("keeps evidence out of repository when private staging is replaced after validation", async () => {
  697|     const simple = createSimpleRepository();
  698|     const outputDir = temporaryOutputPath("ascout-t107-stage-race-");
  699|     const repositoryTarget = join(simple.root, "stage-target");
  700|     mkdirSync(repositoryTarget);
  701|     let replaced = false;
  702| 
  703|     await expect(runSelfVerification({
  704|       repositoryRoot: simple.root,
  705|       eventBaseSha: simple.base,
  706|       headSha: simple.head,
  707|       outputDir,
  708|       testRuntime: runtimeFor(0),
  709|       testEvidenceIo: {
  710|         open: async (...args: Parameters<typeof fsPromises.open>) => {
  711|           const handle = await fsPromises.open(...args);
  712|           if (String(args[0]).endsWith(EVIDENCE_FILES[0])) {
  713|             return {
  714|               writeFile: async (...writeArgs: Parameters<typeof handle.writeFile>) => {
  715|                 if (!replaced) {
  716|                   const stageDir = dirname(String(args[0]));
  717|                   const stageRoot = dirname(stageDir);
  718|                   renameSync(stageDir, join(stageRoot, "displaced-bundle"));
  719|                   symlinkSync(repositoryTarget, stageDir, "dir");
  720|                   replaced = true;
  721|                 }
  722|                 return await handle.writeFile(...writeArgs);
  723|               },
  724|               sync: handle.sync.bind(handle),
  725|               read: handle.read.bind(handle),
  726|               close: handle.close.bind(handle),
  727|             } as unknown as typeof handle;
  728|           }
  729|           return handle;
  730|         },
  731|       },
  732|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  733|     expect(replaced).toBe(true);
  734|     expectNoEvidence(repositoryTarget);
  735|     expectNoEvidence(outputDir);
  736|     expect(existsSync(outputDir)).toBe(false);
  737|   });
  738| 
  739|   it.skipIf(process.platform === "win32")("rejects final output replacement after published identity validation", async () => {
  740|     const simple = createSimpleRepository();
  741|     const outputDir = temporaryOutputPath("ascout-t107-published-race-");
  742|     const repositoryTarget = join(simple.root, "published-target");
  743|     mkdirSync(repositoryTarget);
  744|     const displaced = join(dirname(outputDir), "displaced-published-bundle");
  745|     let finalIdentityChecks = 0;
  746|     let replaced = false;
  747| 
  748|     await expect(runSelfVerification({
  749|       repositoryRoot: simple.root,
  750|       eventBaseSha: simple.base,
  751|       headSha: simple.head,
  752|       outputDir,
  753|       testRuntime: runtimeFor(0),
  754|       testEvidenceIo: {
  755|         lstat: async (...args: Parameters<typeof fsPromises.lstat>) => {
  756|           const stats = await fsPromises.lstat(...args);
  757|           if (String(args[0]) === outputDir) {
  758|             finalIdentityChecks += 1;
  759|             if (finalIdentityChecks === 2 && !replaced) {
  760|               renameSync(outputDir, displaced);
  761|               symlinkSync(repositoryTarget, outputDir, "dir");
  762|               replaced = true;
  763|             }
  764|           }
  765|           return stats;
  766|         },
  767|       },
  768|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  769|     expect(replaced).toBe(true);
  770|     expectNoEvidence(repositoryTarget);
  771|     expectNoEvidence(outputDir);
  772|     expect(existsSync(outputDir)).toBe(false);
  773|   });
  774| 
  775|   it.skipIf(process.platform === "win32")("rolls back output replacement after bound COMMIT checks before parent confirmation", async () => {
  776|     const simple = createSimpleRepository();
  777|     const outputDir = temporaryOutputPath("ascout-t107-post-commit-race-");
  778|     const repositoryTarget = join(simple.root, "post-commit-target");
  779|     const displaced = join(dirname(outputDir), "displaced-post-commit-bundle");
  780|     mkdirSync(repositoryTarget);
  781|     let replaced = false;
  782| 
  783|     await expect(runSelfVerification({
  784|       repositoryRoot: simple.root,
  785|       eventBaseSha: simple.base,
  786|       headSha: simple.head,
  787|       outputDir,
  788|       testRuntime: runtimeFor(0),
  789|       testEvidenceIo: {
  790|         afterBoundParentCommit: async () => {
  791|           renameSync(outputDir, displaced);
  792|           symlinkSync(repositoryTarget, outputDir, "dir");
  793|           replaced = true;
  794|         },
  795|       },
  796|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  797|     expect(replaced).toBe(true);
  798|     expectNoEvidence(repositoryTarget);
  799|     expectNoEvidence(outputDir);
  800|     expect(existsSync(outputDir)).toBe(false);
  801|   });
  802| 
  803|   it.skipIf(process.platform === "win32")("rolls back final pathname replacement after child CONFIRM checks before rollback release", async () => {
  804|     const simple = createSimpleRepository();
  805|     const outputDir = temporaryOutputPath("ascout-t107-post-confirm-race-");
  806|     const repositoryTarget = join(simple.root, "post-confirm-target");
  807|     const displaced = join(dirname(outputDir), "displaced-post-confirm-bundle");
  808|     mkdirSync(repositoryTarget);
  809|     let replaced = false;
  810|     let returnedReceiptPath: string | null = null;
  811| 
  812|     const attempt = runSelfVerification({
  813|       repositoryRoot: simple.root,
  814|       eventBaseSha: simple.base,
  815|       headSha: simple.head,
  816|       outputDir,
  817|       testRuntime: runtimeFor(0),
  818|       testEvidenceIo: {
  819|         afterBoundParentConfirm: async () => {
  820|           renameSync(outputDir, displaced);
  821|           symlinkSync(repositoryTarget, outputDir, "dir");
  822|           replaced = true;
  823|         },
  824|       },
  825|     }).then((result) => {
  826|       returnedReceiptPath = result.receiptPath;
  827|       return result;
  828|     });
  829| 
  830|     await expect(attempt).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  831|     expect(replaced).toBe(true);
  832|     expect(returnedReceiptPath).toBeNull();
  833|     expectNoEvidence(repositoryTarget);
  834|     expectNoEvidence(outputDir);
  835|     expect(existsSync(outputDir)).toBe(false);
  836|   });
  837| 
  838|   it.skipIf(process.platform === "win32")("rolls back final pathname replacement after child RELEASE checks before rollback finalization", async () => {
  839|     const simple = createSimpleRepository();
  840|     const outputDir = temporaryOutputPath("ascout-t107-post-release-race-");
  841|     const repositoryTarget = join(simple.root, "post-release-target");
  842|     const displaced = join(dirname(outputDir), "displaced-post-release-bundle");
  843|     mkdirSync(repositoryTarget);
  844|     let replaced = false;
  845|     let returnedReceiptPath: string | null = null;
  846| 
  847|     const attempt = runSelfVerification({
  848|       repositoryRoot: simple.root,
  849|       eventBaseSha: simple.base,
  850|       headSha: simple.head,
  851|       outputDir,
  852|       testRuntime: runtimeFor(0),
  853|       testEvidenceIo: {
  854|         afterBoundParentRelease: async () => {
  855|           renameSync(outputDir, displaced);
  856|           symlinkSync(repositoryTarget, outputDir, "dir");
  857|           replaced = true;
  858|         },
  859|       },
  860|     }).then((result) => {
  861|       returnedReceiptPath = result.receiptPath;
  862|       return result;
  863|     });
  864| 
  865|     await expect(attempt).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  866|     expect(replaced).toBe(true);
  867|     expect(returnedReceiptPath).toBeNull();
  868|     expectNoEvidence(repositoryTarget);
  869|     expectNoEvidence(outputDir);
  870|     expect(existsSync(outputDir)).toBe(false);
  871|   });
  872| 
  873|   it.skipIf(process.platform === "win32")("rolls back final pathname replacement after child FINALIZE checks without following replacement cleanup", async () => {
  874|     const simple = createSimpleRepository();
  875|     const outputDir = temporaryOutputPath("ascout-t107-post-finalize-race-");
  876|     const repositoryTarget = join(simple.root, "post-finalize-target");
  877|     const displaced = join(dirname(outputDir), "displaced-post-finalize-bundle");
  878|     mkdirSync(repositoryTarget);
  879|     let replaced = false;
  880|     let returnedReceiptPath: string | null = null;
  881|     let recursiveCleanupTouchedReplacement = false;
  882| 
  883|     const attempt = runSelfVerification({
  884|       repositoryRoot: simple.root,
  885|       eventBaseSha: simple.base,
  886|       headSha: simple.head,
  887|       outputDir,
  888|       testRuntime: runtimeFor(0),
  889|       testEvidenceIo: {
  890|         afterBoundParentFinalize: async () => {
  891|           renameSync(outputDir, displaced);
  892|           symlinkSync(repositoryTarget, outputDir, "dir");
  893|           replaced = true;
  894|         },
  895|         rm: async (...args: Parameters<typeof fsPromises.rm>) => {
  896|           if (replaced && String(args[0]) === outputDir) recursiveCleanupTouchedReplacement = true;
  897|           return await fsPromises.rm(...args);
  898|         },
  899|       },
  900|     }).then((result) => {
  901|       returnedReceiptPath = result.receiptPath;
  902|       return result;
  903|     });
  904| 
  905|     await expect(attempt).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_changed"));
  906|     expect(replaced).toBe(true);
  907|     expect(returnedReceiptPath).toBeNull();
  908|     expect(recursiveCleanupTouchedReplacement).toBe(false);
  909|     expectNoEvidence(repositoryTarget);
  910|     expectNoEvidence(outputDir);
  911|     expect(existsSync(outputDir)).toBe(false);
  912|   });
  913| 
  914|   it("removes all published evidence when retained receipt handle read-back mismatches", async () => {
  915|     const simple = createSimpleRepository();
  916|     const outputDir = temporaryOutputPath("ascout-t107-readback-mismatch-");
  917|     let receiptReadPasses = 0;
  918|     await expect(runSelfVerification({
  919|       repositoryRoot: simple.root,
  920|       eventBaseSha: simple.base,
  921|       headSha: simple.head,
  922|       outputDir,
  923|       testRuntime: runtimeFor(0),
  924|       testEvidenceIo: {
  925|         open: async (...args: Parameters<typeof fsPromises.open>) => {
  926|           const handle = await fsPromises.open(...args);
  927|           if (String(args[0]).endsWith(EVIDENCE_FILES[0])) {
  928|             return {
  929|               writeFile: handle.writeFile.bind(handle),
  930|               sync: handle.sync.bind(handle),
  931|               stat: handle.stat.bind(handle),
  932|               read: async (...readArgs: Parameters<typeof handle.read>) => {
  933|                 const result = await handle.read(...readArgs);
  934|                 const position = readArgs[3];
  935|                 if (position === 0) {
  936|                   receiptReadPasses += 1;
  937|                   if (receiptReadPasses >= 2 && result.bytesRead > 0 && Buffer.isBuffer(readArgs[0])) {
  938|                     readArgs[0][0] = readArgs[0][0] ^ 0xff;
  939|                   }
  940|                 }
  941|                 return result;
  942|               },
  943|               close: handle.close.bind(handle),
  944|             } as unknown as typeof handle;
  945|           }
  946|           return handle;
  947|         },
  948|       },
  949|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "receipt_digest_mismatch"));
  950|     expect(receiptReadPasses).toBeGreaterThanOrEqual(2);
  951|     expectNoEvidence(outputDir);
  952|     expect(existsSync(outputDir)).toBe(false);
  953|   }, 15_000);
  954| 
  955|   it("removes all staged evidence when envelope staging fails", async () => {
  956|     const simple = createSimpleRepository();
  957|     const outputDir = temporaryOutputPath("ascout-t107-envelope-failure-");
  958|     await expect(runSelfVerification({
  959|       repositoryRoot: simple.root,
  960|       eventBaseSha: simple.base,
  961|       headSha: simple.head,
  962|       outputDir,
  963|       testRuntime: runtimeFor(0),
  964|       testEvidenceIo: {
  965|         open: async (...args: Parameters<typeof fsPromises.open>) => {
  966|           const handle = await fsPromises.open(...args);
  967|           if (String(args[0]).endsWith(EVIDENCE_FILES[1])) {
  968|             return {
  969|               writeFile: async () => { throw new Error("fixture envelope write failure"); },
  970|               sync: handle.sync.bind(handle),
  971|               close: handle.close.bind(handle),
  972|             } as unknown as typeof handle;
  973|           }
  974|           return handle;
  975|         },
  976|       },
  977|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "evidence_output_failed"));
  978|     expectNoEvidence(outputDir);
  979|     expect(existsSync(outputDir)).toBe(false);
  980|   }, 15_000);
  981| 
  982|   it("rejects evidence output inside repository source identity", async () => {
  983|     const simple = createSimpleRepository();
  984|     await expect(runSelfVerification({
  985|       repositoryRoot: simple.root,
  986|       eventBaseSha: simple.base,
  987|       headSha: simple.head,
  988|       outputDir: join(simple.root, "evidence"),
  989|       testRuntime: runtimeFor(0),
  990|     })).rejects.toSatisfy((error: unknown) => expectIntegrityCode(error, "output_inside_repository"));
  991|   });
  992| 
  993|   it("buildQualificationEnvelope rejects malformed receipt digests", () => {
  994|     expect(() => buildQualificationEnvelope({
  995|       identities: { eventBaseSha: "a".repeat(40), headSha: "b".repeat(40), mergeBaseSha: "a".repeat(40), headTreeSha: "c".repeat(40) },
  996|       receiptExit: 0,
  997|       receiptSha256: "not-a-digest",
  998|     })).toThrowError(/SHA-256/u);
  999|   });
 1000| });
```
