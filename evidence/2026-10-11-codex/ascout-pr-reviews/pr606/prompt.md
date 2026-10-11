You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: 3758ef323601b202d2019129b1cc104138a453be..6f16c76ce3aade747a1ed7afa7e14700e2d2b872 (this PR's own changes relative to its parent branch feat/ua-p06-t09c-source-bound-inventory)
Pull request title (context only): fix(security): reject nonfinite data at T09 JSON observation boundary
Changed files: src/assurance/security/sentrdel-observation-snapshot.ts,tests/assurance-security-t09c.test.ts

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, and whether tests keep their assertion strength.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (1 reviewable / 2 total)

- mode: range
- from: 3758ef323601b202d2019129b1cc104138a453be
- to: 6f16c76ce3aade747a1ed7afa7e14700e2d2b872
- merge_base: 3758ef323601b202d2019129b1cc104138a453be
- total_insertions: 26
- total_deletions: 2

  - `src/assurance/security/sentrdel-observation-snapshot.ts` [modified] +7/-2
~~- `tests/assurance-security-t09c.test.ts` [modified] +19/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- src/assurance/security/sentrdel-observation-snapshot.ts
- tests/assurance-security-t09c.test.ts

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
diff --git a/src/assurance/security/sentrdel-observation-snapshot.ts b/src/assurance/security/sentrdel-observation-snapshot.ts
index 86aa8c4..4cea1df 100644
--- a/src/assurance/security/sentrdel-observation-snapshot.ts
+++ b/src/assurance/security/sentrdel-observation-snapshot.ts
@@ -7,8 +7,13 @@
  */
 export function snapshotSentrdelObservationDataV1(value: unknown, depth = 0): unknown {
   if (depth > 4) throw new TypeError("observation nesting limit exceeded");
-  if (value === null || typeof value === "string" ||
-      typeof value === "boolean" || typeof value === "number") return value;
+  if (value === null || typeof value === "string" || typeof value === "boolean") return value;
+  // JSON has no NaN or infinity. Silently accepting them would convert values
+  // to null during JSON.stringify and corrupt downstream evidence identity.
+  if (typeof value === "number") {
+    if (!Number.isFinite(value)) throw new TypeError("observation number must be finite");
+    return value;
+  }
   if (typeof value !== "object") throw new TypeError("observation must be JSON data");
 
   const isArray = Array.isArray(value);
diff --git a/tests/assurance-security-t09c.test.ts b/tests/assurance-security-t09c.test.ts
index a7553d6..7ad3913 100644
--- a/tests/assurance-security-t09c.test.ts
+++ b/tests/assurance-security-t09c.test.ts
@@ -5,6 +5,7 @@ import {
 } from "../src/assurance/security/sentrdel-t09-inventory.js";
 import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
 import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
+import { snapshotSentrdelObservationDataV1 } from "../src/assurance/security/sentrdel-observation-snapshot.js";
 
 const SHARED = {
   schema_version: 1,
@@ -41,6 +42,24 @@ function configuration(extra: Record<string, unknown> = {}) {
   };
 }
 
+describe("bounded untrusted JSON snapshot", () => {
+  it("rejects non-JSON numeric tokens at every nesting depth", () => {
+    for (const bad of [NaN, Infinity, -Infinity]) {
+      expect(() => snapshotSentrdelObservationDataV1(bad)).toThrow(/finite/);
+      expect(() => snapshotSentrdelObservationDataV1({ record: bad })).toThrow(/finite/);
+      expect(() => snapshotSentrdelObservationDataV1({ records: [1, bad] })).toThrow(/finite/);
+      expect(() => buildSentrdelT09InventoryV1({ workflows: [], configurations: [bad] }))
+        .toThrow(TypeError);
+    }
+  });
+  it("preserves ordinary finite numeric JSON data without granting claims", () => {
+    const data = snapshotSentrdelObservationDataV1({ count: 0, values: [1.25, -0] });
+    expect(data).toEqual({ count: 0, values: [1.25, -0] });
+    expect(Object.isFrozen(data)).toBe(true);
+    expect(JSON.stringify(data)).not.toContain("NaN");
+  });
+});
+
 describe("UA-P06-T09C source/attempt-bound static inventory", () => {
   it("combines only same-source/same-attempt observations with no assurance promotion", () => {
     const result = buildSentrdelT09InventoryV1({
```

## Full file at head: src/assurance/security/sentrdel-observation-snapshot.ts
```
    1| /**
    2|  * Defensive JSON-data snapshot for untrusted in-process observation inputs.
    3|  *
    4|  * Rejects own accessors, hidden/symbol keys, non-plain objects and sparse arrays
    5|  * before validation. This is NOT a process sandbox: Proxy traps and other code
    6|  * already running in this JavaScript process are outside this boundary.
    7|  */
    8| export function snapshotSentrdelObservationDataV1(value: unknown, depth = 0): unknown {
    9|   if (depth > 4) throw new TypeError("observation nesting limit exceeded");
   10|   if (value === null || typeof value === "string" || typeof value === "boolean") return value;
   11|   // JSON has no NaN or infinity. Silently accepting them would convert values
   12|   // to null during JSON.stringify and corrupt downstream evidence identity.
   13|   if (typeof value === "number") {
   14|     if (!Number.isFinite(value)) throw new TypeError("observation number must be finite");
   15|     return value;
   16|   }
   17|   if (typeof value !== "object") throw new TypeError("observation must be JSON data");
   18| 
   19|   const isArray = Array.isArray(value);
   20|   if (!isArray && ![Object.prototype, null].includes(Object.getPrototypeOf(value))) {
   21|     throw new TypeError("observation must be plain JSON data");
   22|   }
   23|   const descriptors = Object.getOwnPropertyDescriptors(value);
   24|   const keys = Reflect.ownKeys(descriptors);
   25|   if (keys.length > 65) throw new TypeError("observation property limit exceeded");
   26|   if (isArray && (value.length > 64 || keys.length !== value.length + 1)) {
   27|     throw new TypeError("observation arrays must be dense and bounded");
   28|   }
   29|   const result: Record<string, unknown> | unknown[] = isArray ? [] : Object.create(null);
   30|   for (const key of keys) {
   31|     if (typeof key !== "string") throw new TypeError("observation symbol keys forbidden");
   32|     if (isArray && key === "length") continue;
   33|     const descriptor = descriptors[key];
   34|     if (!descriptor || !Object.hasOwn(descriptor, "value") || !descriptor.enumerable ||
   35|         key === "__proto__") {
   36|       throw new TypeError("observation requires enumerable own data properties");
   37|     }
   38|     if (isArray && (!/^(0|[1-9][0-9]*)$/u.test(key) ||
   39|         Number(key) >= value.length)) {
   40|       throw new TypeError("observation array keys must be indices");
   41|     }
   42|     Object.defineProperty(result, key, {
   43|       value: snapshotSentrdelObservationDataV1(descriptor.value, depth + 1),
   44|       enumerable: true, configurable: false, writable: false,
   45|     });
   46|   }
   47|   return Object.freeze(result);
   48| }
```

## Full file at head: tests/assurance-security-t09c.test.ts
```
    1| import { describe, expect, it } from "vitest";
    2| import {
    3|   buildSentrdelT09InventoryV1,
    4|   SENTRDEL_T09_MAX_OBSERVATIONS,
    5| } from "../src/assurance/security/sentrdel-t09-inventory.js";
    6| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
    7| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
    8| import { snapshotSentrdelObservationDataV1 } from "../src/assurance/security/sentrdel-observation-snapshot.js";
    9| 
   10| const SHARED = {
   11|   schema_version: 1,
   12|   request_id: "request:test",
   13|   attempt_id: "attempt:test",
   14|   source_head: "a".repeat(40),
   15|   engine_id: SENTRDEL_ENGINE_ID,
   16|   engine_pin: SENTRDEL_PINNED_REVISION,
   17|   engine_tree: SENTRDEL_PINNED_TREE,
   18|   engine_version: SENTRDEL_ENGINE_VERSION,
   19| };
   20| 
   21| function workflow(extra: Record<string, unknown> = {}) {
   22|   return {
   23|     ...SHARED, capability_id: "github-actions", execution_state: "EXECUTED",
   24|     rule_id: "gha.pull-request-target",
   25|     workflow_path: ".github/workflows/ci.yml",
   26|     line: 12,
   27|     producer_id: "producer:fixture", evidence_ref: "evidence:ci",
   28|     evidence_digest: "b".repeat(64),
   29|     coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
   30|     unknown_tokens: [],
   31|     effect_ceiling: "E0_READ_ONLY_ANALYSIS",
   32|     network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS", ...extra,
   33|   };
   34| }
   35| 
   36| function configuration(extra: Record<string, unknown> = {}) {
   37|   return {
   38|     ...SHARED, capability_id: "config-inspection",
   39|     path: ".mcp.json", signal: "mcp-json",
   40|     producer_id: "producer:fixture", evidence_ref: "evidence:mcp",
   41|     evidence_digest: "c".repeat(64), ...extra,
   42|   };
   43| }
   44| 
   45| describe("bounded untrusted JSON snapshot", () => {
   46|   it("rejects non-JSON numeric tokens at every nesting depth", () => {
   47|     for (const bad of [NaN, Infinity, -Infinity]) {
   48|       expect(() => snapshotSentrdelObservationDataV1(bad)).toThrow(/finite/);
   49|       expect(() => snapshotSentrdelObservationDataV1({ record: bad })).toThrow(/finite/);
   50|       expect(() => snapshotSentrdelObservationDataV1({ records: [1, bad] })).toThrow(/finite/);
   51|       expect(() => buildSentrdelT09InventoryV1({ workflows: [], configurations: [bad] }))
   52|         .toThrow(TypeError);
   53|     }
   54|   });
   55|   it("preserves ordinary finite numeric JSON data without granting claims", () => {
   56|     const data = snapshotSentrdelObservationDataV1({ count: 0, values: [1.25, -0] });
   57|     expect(data).toEqual({ count: 0, values: [1.25, -0] });
   58|     expect(Object.isFrozen(data)).toBe(true);
   59|     expect(JSON.stringify(data)).not.toContain("NaN");
   60|   });
   61| });
   62| 
   63| describe("UA-P06-T09C source/attempt-bound static inventory", () => {
   64|   it("combines only same-source/same-attempt observations with no assurance promotion", () => {
   65|     const result = buildSentrdelT09InventoryV1({
   66|       workflows: [workflow()], configurations: [configuration()],
   67|     });
   68|     expect(result.phase_authority).toBe("UA-P06-T09");
   69|     expect(result.source_head).toBe(SHARED.source_head);
   70|     expect(result.engine_pin).toBe(SENTRDEL_PINNED_REVISION);
   71|     expect(result.generic_iac.status).toBe("NOT_RUN");
   72|     expect(result.generic_iac.clean_claimed).toBe(false);
   73|     expect(result.workflow_observations).toHaveLength(1);
   74|     expect(result.config_presence_observations).toHaveLength(1);
   75|     expect(result.assurance_effect).toBe("NONE");
   76|     expect(result.authority).toBe("STATIC_OBSERVATION_INVENTORY_ONLY");
   77|     expect(result.executed_scanner_proven).toBe(false);
   78|     expect(result.coverage_proven_complete).toBe(false);
   79|     expect(result.repository_clean_claimed).toBe(false);
   80|     expect(result.findings_emitted).toBe(false);
   81|     expect(result.claim_assessment_emitted).toBe(false);
   82|     expect(Object.isFrozen(result)).toBe(true);
   83|     expect(Object.isFrozen(result.workflow_observations)).toBe(true);
   84|     expect(Object.isFrozen(result.config_presence_observations)).toBe(true);
   85|     expect(JSON.stringify(result)).not.toMatch(/"PASS"|"SUPPORTED"/u);
   86|   });
   87| 
   88|   it("sorts observation IDs and produces a stable order-independent inventory", () => {
   89|     const workflows = [workflow({ line: 45 }), workflow({ line: 12 })];
   90|     const configurations = [
   91|       configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
   92|       configuration(),
   93|     ];
   94|     const a = buildSentrdelT09InventoryV1({ workflows, configurations });
   95|     const b = buildSentrdelT09InventoryV1({
   96|       workflows: [...workflows].reverse(), configurations: [...configurations].reverse(),
   97|     });
   98|     expect(a).toEqual(b);
   99|     expect(a.inventory_id).toBe(b.inventory_id);
  100|     expect(a.workflow_observations[0]?.observation_id).not.toBe(a.workflow_observations[1]?.observation_id);
  101|     expect(a.config_presence_observations[0]?.identity).not.toBe(a.config_presence_observations[1]?.identity);
  102|   });
  103| 
  104|   it("does not depend on localeCompare or host ICU collation for canonical IDs", () => {
  105|     const values = {
  106|       workflows: [workflow({ line: 45 }), workflow({ line: 12 })],
  107|       configurations: [
  108|         configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
  109|         configuration(),
  110|       ],
  111|     };
  112|     const expected = buildSentrdelT09InventoryV1(values);
  113|     const original = String.prototype.localeCompare;
  114|     try {
  115|       String.prototype.localeCompare = () => {
  116|         throw new Error("locale-specific sorting is forbidden in evidence identity");
  117|       };
  118|       const got = buildSentrdelT09InventoryV1({
  119|         workflows: [...values.workflows].reverse(),
  120|         configurations: [...values.configurations].reverse(),
  121|       });
  122|       expect(got.inventory_id).toBe(expected.inventory_id);
  123|       expect(got.workflow_observations.map(x => x.observation_id)).toEqual(
  124|         expected.workflow_observations.map(x => x.observation_id),
  125|       );
  126|       expect(got.config_presence_observations.map(x => x.identity)).toEqual(
  127|         expected.config_presence_observations.map(x => x.identity),
  128|       );
  129|     } finally {
  130|       String.prototype.localeCompare = original;
  131|     }
  132|   });
  133| 
  134|   it("refuses cross-head and cross-attempt pooling for both record types", () => {
  135|     for (const patch of [
  136|       { source_head: "d".repeat(40) }, { request_id: "request:other" },
  137|       { attempt_id: "attempt:other" },
  138|     ]) {
  139|       expect(() => buildSentrdelT09InventoryV1({
  140|         workflows: [workflow()], configurations: [configuration(patch)],
  141|       })).toThrow(/cross-source/);
  142|       expect(() => buildSentrdelT09InventoryV1({
  143|         workflows: [workflow(patch)], configurations: [configuration()],
  144|       })).toThrow(/cross-source/);
  145|     }
  146|   });
  147| 
  148|   it("refuses duplicate observations rather than inflating coverage", () => {
  149|     expect(() => buildSentrdelT09InventoryV1({
  150|       workflows: [workflow(), workflow()], configurations: [],
  151|     })).toThrow(/repeated evidence/);
  152|     expect(() => buildSentrdelT09InventoryV1({
  153|       workflows: [], configurations: [configuration(), configuration()],
  154|     })).toThrow(/repeated evidence/);
  155|   });
  156| 
  157|   it("refuses unverifiable, malformed, empty, and excessive raw inputs", () => {
  158|     const invalid: unknown[] = [
  159|       null, "PASS", [], {}, { workflows: [], configurations: [] },
  160|       { workflows: [], configurations: [], assessment: "PASS" },
  161|       { workflows: "fake", configurations: [] },
  162|       { workflows: [], configurations: 1 },
  163|       { workflows: [workflow({ rule_id: "gha.fake" })], configurations: [] },
  164|       { workflows: [], configurations: [configuration({ execution_state: "EXECUTED" })] },
  165|       { workflows: [], configurations: [configuration({ source_head: "bad" })] },
  166|       { workflows: [], configurations: [configuration({ path: "../secret" })] },
  167|       { workflows: Array(SENTRDEL_T09_MAX_OBSERVATIONS + 1).fill(workflow()),
  168|         configurations: [] },
  169|     ];
  170|     for (const value of invalid) {
  171|       expect(() => buildSentrdelT09InventoryV1(value)).toThrow(TypeError);
  172|     }
  173|   });
  174| 
  175|   it("refuses accessor, hidden, symbol, and sparse input mutations", () => {
  176|     let observed = 0;
  177|     const getterRecord = { ...workflow() };
  178|     Object.defineProperty(getterRecord, "workflow_path", {
  179|       enumerable: true,
  180|       get() {
  181|         observed += 1;
  182|         return observed < 4 ? ".github/workflows/ci.yml" : "../unsafe.yml";
  183|       },
  184|     });
  185|     const hiddenRecord = { ...configuration() };
  186|     Object.defineProperty(hiddenRecord, "verdict", { value: "PASS", enumerable: false });
  187|     const symbolRecord = { ...configuration(), [Symbol("bypass")]: "PASS" };
  188|     const sparseRecords = Array(1);
  189|     const nestedAccessor = { ...workflow() };
  190|     const unknownTokens: string[] = ["TIMEOUT"];
  191|     Object.defineProperty(unknownTokens, "0", {
  192|       enumerable: true, get: () => "TIMEOUT",
  193|     });
  194|     nestedAccessor.unknown_tokens = unknownTokens;
  195|     for (const input of [
  196|       { workflows: [getterRecord], configurations: [] },
  197|       { workflows: [], configurations: [hiddenRecord] },
  198|       { workflows: [], configurations: [symbolRecord] },
  199|       { workflows: sparseRecords, configurations: [] },
  200|       { workflows: [nestedAccessor], configurations: [] },
  201|     ]) {
  202|       expect(() => buildSentrdelT09InventoryV1(input)).toThrow(TypeError);
  203|     }
  204|     expect(observed).toBe(0);
  205|   });
  206| 
  207|   it("accepts a single characterized surface without inferring the absent one was checked", () => {
  208|     const a = buildSentrdelT09InventoryV1({ workflows: [workflow()], configurations: [] });
  209|     const b = buildSentrdelT09InventoryV1({ workflows: [], configurations: [configuration()] });
  210|     expect(a.workflow_observations).toHaveLength(1);
  211|     expect(a.config_presence_observations).toHaveLength(0);
  212|     expect(b.workflow_observations).toHaveLength(0);
  213|     expect(b.config_presence_observations).toHaveLength(1);
  214|     expect(a.coverage_proven_complete).toBe(false);
  215|     expect(b.coverage_proven_complete).toBe(false);
  216|     expect(a.generic_iac.status).toBe("NOT_RUN");
  217|     expect(b.generic_iac.status).toBe("NOT_RUN");
  218|   });
  219| });
```
