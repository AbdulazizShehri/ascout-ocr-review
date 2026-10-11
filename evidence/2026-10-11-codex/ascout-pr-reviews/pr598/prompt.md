You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: 1b03e0e95bce03f2c3cf6f0db905ba1faa96fadb..80d75cfa7e4c49810ccd4faa012f0497890bf81d (this PR's own changes relative to its parent branch feat/ua-p06-t09a-workflow-observation)
Pull request title (context only): security(t09): protect standalone untrusted observation normalizers
Changed files: src/assurance/security/sentrdel-observation-snapshot.ts,src/assurance/security/sentrdel-workflow-normalization.ts,tests/assurance-security-t09a.test.ts

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, and whether tests keep their assertion strength.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (2 reviewable / 3 total)

- mode: range
- from: 1b03e0e95bce03f2c3cf6f0db905ba1faa96fadb
- to: 80d75cfa7e4c49810ccd4faa012f0497890bf81d
- merge_base: 1b03e0e95bce03f2c3cf6f0db905ba1faa96fadb
- total_insertions: 117
- total_deletions: 3

  - `src/assurance/security/sentrdel-observation-snapshot.ts` [added] +47/-0
  - `src/assurance/security/sentrdel-workflow-normalization.ts` [modified] +20/-3
~~- `tests/assurance-security-t09a.test.ts` [modified] +50/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- src/assurance/security/sentrdel-observation-snapshot.ts
- src/assurance/security/sentrdel-workflow-normalization.ts
- tests/assurance-security-t09a.test.ts

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
new file mode 100644
index 0000000..d9f07d5
--- /dev/null
+++ b/src/assurance/security/sentrdel-observation-snapshot.ts
@@ -0,0 +1,47 @@
+/**
+ * Defensive JSON-data snapshot for untrusted in-process observation inputs.
+ *
+ * Rejects own accessors, hidden/symbol keys, non-plain objects and sparse arrays
+ * before validation. This is NOT a process sandbox: Proxy traps and other code
+ * already running in this JavaScript process are outside this boundary.
+ */
+export function snapshotSentrdelObservationDataV1(value: unknown, depth = 0): unknown {
+  if (depth > 4) throw new TypeError("observation nesting limit exceeded");
+  if (value === null || typeof value === "string" ||
+      typeof value === "boolean" || typeof value === "number") return value;
+  if (typeof value !== "object") throw new TypeError("observation must be JSON data");
+
+  const isArray = Array.isArray(value);
+  if (!isArray && ![Object.prototype, null].includes(Object.getPrototypeOf(value))) {
+    throw new TypeError("observation must be plain JSON data");
+  }
+  const descriptors = Object.getOwnPropertyDescriptors(value);
+  const keys = Reflect.ownKeys(descriptors);
+  if (keys.length > 65) throw new TypeError("observation property limit exceeded");
+  // Use the captured `length` descriptor only. A fresh `value.length` read can
+  // reach a Proxy `get` trap and differ between checks, admitting a sparse array.
+  const length: unknown = isArray ? descriptors["length" as keyof typeof descriptors]?.value : 0;
+  if (isArray && (typeof length !== "number" || !Number.isSafeInteger(length) ||
+      length > 64 || keys.length !== length + 1)) {
+    throw new TypeError("observation arrays must be dense and bounded");
+  }
+  const result: Record<string, unknown> | unknown[] = isArray ? [] : Object.create(null);
+  for (const key of keys) {
+    if (typeof key !== "string") throw new TypeError("observation symbol keys forbidden");
+    if (isArray && key === "length") continue;
+    const descriptor = descriptors[key];
+    if (!descriptor || !Object.hasOwn(descriptor, "value") || !descriptor.enumerable ||
+        key === "__proto__") {
+      throw new TypeError("observation requires enumerable own data properties");
+    }
+    if (isArray && (!/^(0|[1-9][0-9]*)$/u.test(key) ||
+        Number(key) >= (length as number))) {
+      throw new TypeError("observation array keys must be indices");
+    }
+    Object.defineProperty(result, key, {
+      value: snapshotSentrdelObservationDataV1(descriptor.value, depth + 1),
+      enumerable: true, configurable: false, writable: false,
+    });
+  }
+  return Object.freeze(result);
+}
diff --git a/src/assurance/security/sentrdel-workflow-normalization.ts b/src/assurance/security/sentrdel-workflow-normalization.ts
index f30ae74..e0bba40 100644
--- a/src/assurance/security/sentrdel-workflow-normalization.ts
+++ b/src/assurance/security/sentrdel-workflow-normalization.ts
@@ -7,6 +7,7 @@
  * generic IaC remains unsupported and must be reported separately.
  */
 import { createHash } from "node:crypto";
+import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
 import {
   buildSentrdelCapabilitiesV1,
   getSentrdelCapabilityV1,
@@ -113,7 +114,7 @@ function record(value: unknown): value is Record<string, unknown> {
   return typeof value === "object" && value !== null && !Array.isArray(value);
 }
 
-export function validateSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflowValidationV1 {
+function validatePlainSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflowValidationV1 {
   const reasons: string[] = [];
   if (!record(input)) {
     return { valid: false, reasons: Object.freeze(["input must be a record"]) };
@@ -175,13 +176,29 @@ export function validateSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflo
   return Object.freeze({ valid: reasons.length === 0, reasons: Object.freeze(reasons) });
 }
 
+/**
+ * Validate a stable snapshot; invalid accessors/hidden data fail closed without
+ * running getters. All exported entry points enforce this boundary themselves.
+ */
+export function validateSentrdelWorkflowInputV1(value: unknown): SentrdelWorkflowValidationV1 {
+  try {
+    return validatePlainSentrdelWorkflowInputV1(snapshotSentrdelObservationDataV1(value));
+  } catch {
+    return Object.freeze({
+      valid: false,
+      reasons: Object.freeze(["input must be immutable plain JSON data"]),
+    });
+  }
+}
+
 /** This is data normalization, not a scan, review result, or proof of runtime execution. */
 export function normalizeSentrdelWorkflowObservationV1(
   value: unknown,
 ): SentrdelWorkflowObservationV1 {
-  const check = validateSentrdelWorkflowInputV1(value);
+  const stable = snapshotSentrdelObservationDataV1(value);
+  const check = validatePlainSentrdelWorkflowInputV1(stable);
   if (!check.valid) throw new TypeError(`invalid workflow observation: ${check.reasons.join("; ")}`);
-  const input = value as SentrdelWorkflowInputV1;
+  const input = stable as SentrdelWorkflowInputV1;
   const unknown = Object.freeze([...input.unknown_tokens].sort());
   const identity = [
     SENTRDEL_WORKFLOW_PHASE_AUTHORITY, input.request_id, input.attempt_id,
diff --git a/tests/assurance-security-t09a.test.ts b/tests/assurance-security-t09a.test.ts
index f656504..0cb6020 100644
--- a/tests/assurance-security-t09a.test.ts
+++ b/tests/assurance-security-t09a.test.ts
@@ -147,6 +147,56 @@ describe("UA-P06-T09A bounded CI observation normalization", () => {
     }
   });
 
+  it("refuses accessor-driven identity changes at direct entry points", () => {
+    let getterCalls = 0;
+    const accessor = { ...input() };
+    Object.defineProperty(accessor, "source_head", {
+      enumerable: true,
+      get() {
+        getterCalls += 1;
+        return getterCalls < 2 ? "a".repeat(40) : "b".repeat(40);
+      },
+    });
+    expect(validateSentrdelWorkflowInputV1(accessor).valid).toBe(false);
+    expect(() => normalizeSentrdelWorkflowObservationV1(accessor)).toThrow(TypeError);
+    expect(getterCalls).toBe(0);
+
+    const hidden = { ...input() };
+    Object.defineProperty(hidden, "assurance_override", { value: "PASS", enumerable: false });
+    const symbolic = { ...input(), [Symbol("authority")]: "SUPPORTED" };
+    const sparse = Array(1);
+    const nested = ["TIMEOUT"];
+    Object.defineProperty(nested, "0", { enumerable: true, get: () => "TIMEOUT" });
+    for (const candidate of [hidden, symbolic, input({ unknown_tokens: sparse }),
+      input({ unknown_tokens: nested })]) {
+      expect(validateSentrdelWorkflowInputV1(candidate).valid).toBe(false);
+      expect(() => normalizeSentrdelWorkflowObservationV1(candidate)).toThrow(TypeError);
+    }
+    expect(normalizeSentrdelWorkflowObservationV1(input()).authority)
+      .toBe("CONFIG_OBSERVATION_ONLY");
+  });
+
+  it("uses the captured array length, so a Proxy cannot smuggle a hole past validation", () => {
+    // Keys 0 and 2 only. The `get` trap answers `length` with 2 on the read that
+    // compares the key count and 3 afterwards; any fresh read admits the hole.
+    const lyingTokens = () => {
+      const target: string[] = ["PARSER_UNSUPPORTED", "x", "TIMEOUT"];
+      delete (target as unknown as Record<string, unknown>)[1];
+      let reads = 0;
+      return new Proxy(target, {
+        get(t, key, receiver) {
+          if (key === "length") return ++reads === 2 ? 2 : 3;
+          return Reflect.get(t, key, receiver);
+        },
+      });
+    };
+    const candidate = input({ coverage_state: "PARTIAL", unknown_tokens: lyingTokens() });
+    expect(validateSentrdelWorkflowInputV1(candidate).valid).toBe(false);
+    expect(() => normalizeSentrdelWorkflowObservationV1(
+      input({ coverage_state: "PARTIAL", unknown_tokens: lyingTokens() }),
+    )).toThrow(TypeError);
+  });
+
   it("refuses malformed nonrecord input and unknown arrays", () => {
     for (const value of [null, undefined, [], 1, "ready"]) {
       expect(validateSentrdelWorkflowInputV1(value).valid).toBe(false);
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
   10|   if (value === null || typeof value === "string" ||
   11|       typeof value === "boolean" || typeof value === "number") return value;
   12|   if (typeof value !== "object") throw new TypeError("observation must be JSON data");
   13| 
   14|   const isArray = Array.isArray(value);
   15|   if (!isArray && ![Object.prototype, null].includes(Object.getPrototypeOf(value))) {
   16|     throw new TypeError("observation must be plain JSON data");
   17|   }
   18|   const descriptors = Object.getOwnPropertyDescriptors(value);
   19|   const keys = Reflect.ownKeys(descriptors);
   20|   if (keys.length > 65) throw new TypeError("observation property limit exceeded");
   21|   // Use the captured `length` descriptor only. A fresh `value.length` read can
   22|   // reach a Proxy `get` trap and differ between checks, admitting a sparse array.
   23|   const length: unknown = isArray ? descriptors["length" as keyof typeof descriptors]?.value : 0;
   24|   if (isArray && (typeof length !== "number" || !Number.isSafeInteger(length) ||
   25|       length > 64 || keys.length !== length + 1)) {
   26|     throw new TypeError("observation arrays must be dense and bounded");
   27|   }
   28|   const result: Record<string, unknown> | unknown[] = isArray ? [] : Object.create(null);
   29|   for (const key of keys) {
   30|     if (typeof key !== "string") throw new TypeError("observation symbol keys forbidden");
   31|     if (isArray && key === "length") continue;
   32|     const descriptor = descriptors[key];
   33|     if (!descriptor || !Object.hasOwn(descriptor, "value") || !descriptor.enumerable ||
   34|         key === "__proto__") {
   35|       throw new TypeError("observation requires enumerable own data properties");
   36|     }
   37|     if (isArray && (!/^(0|[1-9][0-9]*)$/u.test(key) ||
   38|         Number(key) >= (length as number))) {
   39|       throw new TypeError("observation array keys must be indices");
   40|     }
   41|     Object.defineProperty(result, key, {
   42|       value: snapshotSentrdelObservationDataV1(descriptor.value, depth + 1),
   43|       enumerable: true, configurable: false, writable: false,
   44|     });
   45|   }
   46|   return Object.freeze(result);
   47| }
```

## Full file at head: src/assurance/security/sentrdel-workflow-normalization.ts
```
    1| /**
    2|  * UA-P06-T09, grain A — bounded GitHub Actions observation normalization.
    3|  *
    4|  * This module consumes untrusted records. It does not execute a scanner,
    5|  * interpret an action, validate a vulnerability, or issue assurance claims.
    6|  * The pinned producer supports a subset of changed GitHub Actions workflows;
    7|  * generic IaC remains unsupported and must be reported separately.
    8|  */
    9| import { createHash } from "node:crypto";
   10| import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
   11| import {
   12|   buildSentrdelCapabilitiesV1,
   13|   getSentrdelCapabilityV1,
   14| } from "./sentrdel-capability-characterization.js";
   15| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "./sentrdel-engine-boundary.js";
   16| import { containsSecretMaterialV1, containsExternalAttestationV1 } from "./sentrdel-evidence-normalization.js";
   17| import { SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES } from "./sentrdel-engine-adapter.js";
   18| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE, SENTRDEL_PIN_REF } from "./sentrdel-source-pin.js";
   19| 
   20| export const SENTRDEL_WORKFLOW_PHASE_AUTHORITY = "UA-P06-T09" as const;
   21| export const SENTRDEL_WORKFLOW_CAPABILITY_ID = "github-actions" as const;
   22| export const SENTRDEL_GENERIC_IAC_CAPABILITY_ID = "iac-generic" as const;
   23| 
   24| /** Rule IDs observed in the exact pinned donor github_actions.rs implementation. */
   25| export const SENTRDEL_WORKFLOW_RULE_IDS = Object.freeze([
   26|   "gha.permission-widening",
   27|   "gha.oidc-id-token-write",
   28|   "gha.pull-request-target",
   29|   "gha.secret-in-untrusted-pr-path",
   30|   "gha.untrusted-expression-shell",
   31|   "gha.mutable-action-ref",
   32|   "gha.self-hosted-runner-change",
   33|   "gha.trust-sensitive-artifact-cache-handoff",
   34| ] as const);
   35| 
   36| const RULE_SET: ReadonlySet<string> = new Set(SENTRDEL_WORKFLOW_RULE_IDS);
   37| const CAPABILITIES = buildSentrdelCapabilitiesV1();
   38| const WORKFLOW = getSentrdelCapabilityV1(CAPABILITIES, "github-actions");
   39| const GENERIC_IAC = getSentrdelCapabilityV1(CAPABILITIES, "iac-generic");
   40| const UNKNOWN_SET = new Set<string>(WORKFLOW?.unknown_tokens ?? []);
   41| const SHA1 = /^[a-f0-9]{40}$/u;
   42| const SHA256 = /^[a-f0-9]{64}$/u;
   43| const ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
   44| const PATH = /^\.github\/workflows\/[A-Za-z0-9_.-]+\.ya?ml$/u;
   45| const KEYS = Object.freeze([
   46|   "schema_version", "request_id", "attempt_id", "source_head", "engine_id",
   47|   "engine_pin", "engine_tree", "engine_version", "capability_id", "execution_state",
   48|   "rule_id", "workflow_path", "line", "producer_id", "evidence_ref",
   49|   "evidence_digest", "coverage_state", "unknown_tokens",
   50|   "effect_ceiling", "network_policy", "egress_policy",
   51| ] as const);
   52| 
   53| export interface SentrdelWorkflowInputV1 {
   54|   readonly schema_version: 1;
   55|   readonly request_id: string;
   56|   readonly attempt_id: string;
   57|   readonly source_head: string;
   58|   readonly engine_id: typeof SENTRDEL_ENGINE_ID;
   59|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   60|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   61|   readonly engine_version: typeof SENTRDEL_ENGINE_VERSION;
   62|   readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
   63|   readonly execution_state: "EXECUTED";
   64|   readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
   65|   readonly workflow_path: string;
   66|   readonly line: number;
   67|   readonly producer_id: string;
   68|   readonly evidence_ref: string;
   69|   readonly evidence_digest: string;
   70|   readonly coverage_state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
   71|   readonly unknown_tokens: readonly string[];
   72|   readonly effect_ceiling: "E0_READ_ONLY_ANALYSIS";
   73|   readonly network_policy: "NO_NETWORK";
   74|   readonly egress_policy: "NO_EGRESS";
   75| }
   76| 
   77| export interface SentrdelWorkflowObservationV1 {
   78|   readonly schema_version: 1;
   79|   readonly phase_authority: typeof SENTRDEL_WORKFLOW_PHASE_AUTHORITY;
   80|   readonly observation_id: string;
   81|   readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
   82|   readonly source_head: string;
   83|   readonly request_id: string;
   84|   readonly attempt_id: string;
   85|   readonly engine_id: typeof SENTRDEL_ENGINE_ID;
   86|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   87|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   88|   readonly engine_pin_ref: typeof SENTRDEL_PIN_REF;
   89|   readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
   90|   readonly workflow_path: string;
   91|   readonly line: number;
   92|   readonly provenance: Readonly<{ producer_id: string; evidence_ref: string; evidence_digest: string }>;
   93|   readonly coverage: Readonly<{
   94|     state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
   95|     unknown_tokens: readonly string[];
   96|     repository_total: false;
   97|     unscanned_is_clean: false;
   98|   }>;
   99|   readonly authority: "CONFIG_OBSERVATION_ONLY";
  100|   readonly assurance_effect: "NONE";
  101|   readonly finding_emitted: false;
  102|   readonly claim_assessment_emitted: false;
  103|   readonly producer_execution_attested: false;
  104|   readonly severity_derived: false;
  105|   readonly remediation_verified: false;
  106| }
  107| 
  108| export interface SentrdelWorkflowValidationV1 {
  109|   readonly valid: boolean;
  110|   readonly reasons: readonly string[];
  111| }
  112| 
  113| function record(value: unknown): value is Record<string, unknown> {
  114|   return typeof value === "object" && value !== null && !Array.isArray(value);
  115| }
  116| 
  117| function validatePlainSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflowValidationV1 {
  118|   const reasons: string[] = [];
  119|   if (!record(input)) {
  120|     return { valid: false, reasons: Object.freeze(["input must be a record"]) };
  121|   }
  122|   const expected = new Set<string>(KEYS);
  123|   if (Object.keys(input).length !== KEYS.length ||
  124|       Object.keys(input).some((key) => !expected.has(key))) {
  125|     reasons.push("input keys must match the exact bounded schema");
  126|   }
  127|   const exact: Readonly<Record<string, unknown>> = {
  128|     schema_version: 1, engine_id: SENTRDEL_ENGINE_ID,
  129|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
  130|     engine_version: SENTRDEL_ENGINE_VERSION, capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID,
  131|     execution_state: "EXECUTED", effect_ceiling: "E0_READ_ONLY_ANALYSIS",
  132|     network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS",
  133|   };
  134|   for (const [key, expectedValue] of Object.entries(exact)) {
  135|     if (input[key] !== expectedValue) reasons.push(`${key} does not match the pinned boundary`);
  136|   }
  137|   for (const key of ["request_id", "attempt_id", "producer_id", "evidence_ref"]) {
  138|     if (typeof input[key] !== "string" || !ID.test(input[key])) reasons.push(`${key} is invalid`);
  139|   }
  140|   if (typeof input["source_head"] !== "string" || !SHA1.test(input["source_head"])) {
  141|     reasons.push("source_head must be a canonical Git SHA-1");
  142|   }
  143|   if (typeof input["evidence_digest"] !== "string" || !SHA256.test(input["evidence_digest"])) {
  144|     reasons.push("evidence_digest must be a SHA-256 digest");
  145|   }
  146|   if (!RULE_SET.has(input["rule_id"] as string)) reasons.push("rule_id is not present at the pinned donor");
  147|   if (typeof input["workflow_path"] !== "string" || !PATH.test(input["workflow_path"])) {
  148|     reasons.push("workflow_path must be a canonical changed GitHub Actions YAML path");
  149|   }
  150|   if (!Number.isSafeInteger(input["line"]) || (input["line"] as number) < 1 ||
  151|       (input["line"] as number) > 1_000_000) reasons.push("line must be a bounded positive integer");
  152|   if (input["coverage_state"] !== "COMPLETE_WITHIN_STATED_SCOPE" &&
  153|       input["coverage_state"] !== "PARTIAL") reasons.push("coverage_state must be executed-scope coverage");
  154|   const tokens = input["unknown_tokens"];
  155|   if (!Array.isArray(tokens) || tokens.length > 8 ||
  156|       tokens.some((item: unknown) => typeof item !== "string" || !UNKNOWN_SET.has(item)) ||
  157|       new Set(tokens).size !== tokens.length) {
  158|     reasons.push("unknown_tokens must be unique characterized tokens");
  159|   } else if (tokens.length > 0 && input["coverage_state"] !== "PARTIAL") {
  160|     reasons.push("unknown tokens cannot be reported as complete coverage");
  161|   } else if (tokens.length === 0 && input["coverage_state"] === "PARTIAL") {
  162|     reasons.push("partial coverage must declare its unknown reason");
  163|   }
  164| 
  165|   if (WORKFLOW?.status !== "CHARACTERIZED" ||
  166|       !SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("github-actions")) {
  167|     reasons.push("pinned workflow capability is not characterized and adapter-admitted");
  168|   }
  169|   for (const value of Object.values(input)) {
  170|     if (typeof value === "string" &&
  171|         (containsSecretMaterialV1(value) || containsExternalAttestationV1(value))) {
  172|       reasons.push("untrusted strings may not contain secrets or self-attestation");
  173|       break;
  174|     }
  175|   }
  176|   return Object.freeze({ valid: reasons.length === 0, reasons: Object.freeze(reasons) });
  177| }
  178| 
  179| /**
  180|  * Validate a stable snapshot; invalid accessors/hidden data fail closed without
  181|  * running getters. All exported entry points enforce this boundary themselves.
  182|  */
  183| export function validateSentrdelWorkflowInputV1(value: unknown): SentrdelWorkflowValidationV1 {
  184|   try {
  185|     return validatePlainSentrdelWorkflowInputV1(snapshotSentrdelObservationDataV1(value));
  186|   } catch {
  187|     return Object.freeze({
  188|       valid: false,
  189|       reasons: Object.freeze(["input must be immutable plain JSON data"]),
  190|     });
  191|   }
  192| }
  193| 
  194| /** This is data normalization, not a scan, review result, or proof of runtime execution. */
  195| export function normalizeSentrdelWorkflowObservationV1(
  196|   value: unknown,
  197| ): SentrdelWorkflowObservationV1 {
  198|   const stable = snapshotSentrdelObservationDataV1(value);
  199|   const check = validatePlainSentrdelWorkflowInputV1(stable);
  200|   if (!check.valid) throw new TypeError(`invalid workflow observation: ${check.reasons.join("; ")}`);
  201|   const input = stable as SentrdelWorkflowInputV1;
  202|   const unknown = Object.freeze([...input.unknown_tokens].sort());
  203|   const identity = [
  204|     SENTRDEL_WORKFLOW_PHASE_AUTHORITY, input.request_id, input.attempt_id,
  205|     input.engine_pin, input.engine_tree, input.engine_version,
  206|     input.source_head, input.rule_id, input.workflow_path,
  207|     String(input.line), input.producer_id, input.evidence_ref,
  208|     input.evidence_digest, input.coverage_state, ...unknown,
  209|   ];
  210|   const digest = createHash("sha256").update(JSON.stringify(identity), "utf8").digest("hex");
  211|   return Object.freeze({
  212|     schema_version: 1, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
  213|     observation_id: `ci-observation:sentrdel:${digest}`,
  214|     capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID, source_head: input.source_head,
  215|     request_id: input.request_id, attempt_id: input.attempt_id,
  216|     engine_id: SENTRDEL_ENGINE_ID, engine_pin: SENTRDEL_PINNED_REVISION,
  217|     engine_tree: SENTRDEL_PINNED_TREE, engine_pin_ref: SENTRDEL_PIN_REF,
  218|     rule_id: input.rule_id, workflow_path: input.workflow_path, line: input.line,
  219|     provenance: Object.freeze({
  220|       producer_id: input.producer_id, evidence_ref: input.evidence_ref,
  221|       evidence_digest: input.evidence_digest,
  222|     }),
  223|     coverage: Object.freeze({
  224|       state: input.coverage_state, unknown_tokens: unknown,
  225|       repository_total: false as const, unscanned_is_clean: false as const,
  226|     }),
  227|     authority: "CONFIG_OBSERVATION_ONLY" as const,
  228|     assurance_effect: "NONE" as const, finding_emitted: false as const,
  229|     claim_assessment_emitted: false as const, producer_execution_attested: false as const,
  230|     severity_derived: false as const, remediation_verified: false as const,
  231|   });
  232| }
  233| 
  234| /** The pinned Sentrdel implementation has no generic IaC producer. */
  235| export function buildSentrdelGenericIacGapV1() {
  236|   if (GENERIC_IAC?.status !== "UNSUPPORTED" ||
  237|       SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("iac-generic")) {
  238|     throw new TypeError("pinned generic IaC characterization drifted");
  239|   }
  240|   return Object.freeze({
  241|     schema_version: 1 as const, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
  242|     capability_id: SENTRDEL_GENERIC_IAC_CAPABILITY_ID,
  243|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
  244|     status: "NOT_RUN" as const, reason_code: "unsupported_at_pinned_source" as const,
  245|     reason_text: "No generic IaC analyzer is implemented at the pinned Sentrdel revision.",
  246|     coverage_total: false as const, clean_claimed: false as const,
  247|     assurance_effect: "NONE" as const,
  248|   });
  249| }
```

## Full file at head: tests/assurance-security-t09a.test.ts
```
    1| import { describe, expect, it } from "vitest";
    2| import {
    3|   SENTRDEL_WORKFLOW_RULE_IDS,
    4|   buildSentrdelGenericIacGapV1,
    5|   normalizeSentrdelWorkflowObservationV1,
    6|   validateSentrdelWorkflowInputV1,
    7|   type SentrdelWorkflowInputV1,
    8| } from "../src/assurance/security/sentrdel-workflow-normalization.js";
    9| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
   10| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
   11| 
   12| const HEAD = "a".repeat(40);
   13| const DIGEST = "b".repeat(64);
   14| 
   15| function input(overrides: Record<string, unknown> = {}): SentrdelWorkflowInputV1 {
   16|   return {
   17|     schema_version: 1,
   18|     request_id: "request:fixture",
   19|     attempt_id: "attempt:fixture",
   20|     source_head: HEAD,
   21|     engine_id: SENTRDEL_ENGINE_ID,
   22|     engine_pin: SENTRDEL_PINNED_REVISION,
   23|     engine_tree: SENTRDEL_PINNED_TREE,
   24|     engine_version: SENTRDEL_ENGINE_VERSION,
   25|     capability_id: "github-actions",
   26|     execution_state: "EXECUTED",
   27|     rule_id: "gha.pull-request-target",
   28|     workflow_path: ".github/workflows/ci.yml",
   29|     line: 17,
   30|     producer_id: "producer:sentrdel",
   31|     evidence_ref: "evidence:synthetic",
   32|     evidence_digest: DIGEST,
   33|     coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
   34|     unknown_tokens: [],
   35|     effect_ceiling: "E0_READ_ONLY_ANALYSIS",
   36|     network_policy: "NO_NETWORK",
   37|     egress_policy: "NO_EGRESS",
   38|     ...overrides,
   39|   } as SentrdelWorkflowInputV1;
   40| }
   41| 
   42| describe("UA-P06-T09A bounded CI observation normalization", () => {
   43|   it("accepts each actual pinned GitHub Actions rule identifier", () => {
   44|     expect(SENTRDEL_WORKFLOW_RULE_IDS).toHaveLength(8);
   45|     for (const rule of SENTRDEL_WORKFLOW_RULE_IDS) {
   46|       const record = normalizeSentrdelWorkflowObservationV1(input({ rule_id: rule }));
   47|       expect(record.rule_id).toBe(rule);
   48|       expect(record.phase_authority).toBe("UA-P06-T09");
   49|       expect(record.authority).toBe("CONFIG_OBSERVATION_ONLY");
   50|       expect(record.assurance_effect).toBe("NONE");
   51|       expect(record.finding_emitted).toBe(false);
   52|       expect(record.claim_assessment_emitted).toBe(false);
   53|       expect(record.producer_execution_attested).toBe(false);
   54|       expect(record.severity_derived).toBe(false);
   55|       expect(record.remediation_verified).toBe(false);
   56|       expect(record.coverage.repository_total).toBe(false);
   57|       expect(record.coverage.unscanned_is_clean).toBe(false);
   58|       expect(JSON.stringify(record)).not.toMatch(/"PASS"|"SUPPORTED"|"CLEAN"/u);
   59|     }
   60|   });
   61| 
   62|   it("is deterministic, frozen, and bound to exact source and evidence identity", () => {
   63|     const source = input();
   64|     const first = normalizeSentrdelWorkflowObservationV1(source);
   65|     expect(normalizeSentrdelWorkflowObservationV1(source)).toEqual(first);
   66|     expect(Object.isFrozen(first)).toBe(true);
   67|     expect(Object.isFrozen(first.provenance)).toBe(true);
   68|     expect(Object.isFrozen(first.coverage)).toBe(true);
   69|     expect(Object.isFrozen(first.coverage.unknown_tokens)).toBe(true);
   70|     expect(normalizeSentrdelWorkflowObservationV1(input({ source_head: "c".repeat(40) })).observation_id)
   71|       .not.toBe(first.observation_id);
   72|     expect(normalizeSentrdelWorkflowObservationV1(input({ evidence_digest: "d".repeat(64) })).observation_id)
   73|       .not.toBe(first.observation_id);
   74|     expect(normalizeSentrdelWorkflowObservationV1(input({ attempt_id: "attempt:other" })).observation_id)
   75|       .not.toBe(first.observation_id);
   76|     expect(normalizeSentrdelWorkflowObservationV1(input({ producer_id: "producer:other" })).observation_id)
   77|       .not.toBe(first.observation_id);
   78|     expect(normalizeSentrdelWorkflowObservationV1(input({ evidence_ref: "evidence:other" })).observation_id)
   79|       .not.toBe(first.observation_id);
   80|   });
   81| 
   82|   it("preserves partial coverage and canonicalizes unknown reasons", () => {
   83|     const a = input({ coverage_state: "PARTIAL", unknown_tokens: ["TIMEOUT", "PARSER_UNSUPPORTED"] });
   84|     const b = input({ coverage_state: "PARTIAL", unknown_tokens: ["PARSER_UNSUPPORTED", "TIMEOUT"] });
   85|     const x = normalizeSentrdelWorkflowObservationV1(a);
   86|     expect(x).toEqual(normalizeSentrdelWorkflowObservationV1(b));
   87|     expect(x.coverage.unknown_tokens).toEqual(["PARSER_UNSUPPORTED", "TIMEOUT"]);
   88|     expect(x.coverage.state).toBe("PARTIAL");
   89|     expect(x.coverage.repository_total).toBe(false);
   90|   });
   91| 
   92|   it("never promotes generic IaC absence into clean/supported scope", () => {
   93|     const gap = buildSentrdelGenericIacGapV1();
   94|     expect(gap.capability_id).toBe("iac-generic");
   95|     expect(gap.phase_authority).toBe("UA-P06-T09");
   96|     expect(gap.status).toBe("NOT_RUN");
   97|     expect(gap.reason_code).toBe("unsupported_at_pinned_source");
   98|     expect(gap.coverage_total).toBe(false);
   99|     expect(gap.clean_claimed).toBe(false);
  100|     expect(gap.assurance_effect).toBe("NONE");
  101|     expect(Object.isFrozen(gap)).toBe(true);
  102|     expect(buildSentrdelGenericIacGapV1()).toEqual(gap);
  103|   });
  104| 
  105|   it("refuses unqualified and escalation-bearing observation input", () => {
  106|     const invalid: Array<[string, Record<string, unknown>]> = [
  107|       ["engine pin", { engine_pin: "0".repeat(40) }],
  108|       ["engine tree", { engine_tree: "0".repeat(40) }],
  109|       ["engine identity", { engine_id: "engine:other" }],
  110|       ["version", { engine_version: "99.0.0" }],
  111|       ["capability", { capability_id: "iac-generic" }],
  112|       ["unsupported CI format", { capability_id: "jenkins" }],
  113|       ["absent engine", { execution_state: "UNAVAILABLE" }],
  114|       ["timeout", { execution_state: "TIMEOUT" }],
  115|       ["engine error", { execution_state: "ENGINE_ERROR" }],
  116|       ["invented rule", { rule_id: "gha.does-not-exist" }],
  117|       ["absolute path", { workflow_path: "C:/private/workflow.yml" }],
  118|       ["parent traversal", { workflow_path: ".github/workflows/../ci.yml" }],
  119|       ["arbitrary YAML", { workflow_path: "config/ci.yml" }],
  120|       ["nested workflow path", { workflow_path: ".github/workflows/tmp/ci.yml" }],
  121|       ["unsafe path", { workflow_path: ".github/workflows/ci ; echo unsafe.yml" }],
  122|       ["invalid line", { line: 0 }],
  123|       ["noninteger line", { line: 1.5 }],
  124|       ["overflow line", { line: 1_000_001 }],
  125|       ["missing provenance", { producer_id: "" }],
  126|       ["missing evidence", { evidence_ref: "" }],
  127|       ["bad evidence digest", { evidence_digest: "123" }],
  128|       ["invalid head", { source_head: "123" }],
  129|       ["fabricated coverage", { coverage_state: "TOTAL" }],
  130|       ["unexplained partial", { coverage_state: "PARTIAL", unknown_tokens: [] }],
  131|       ["unknown in complete", { coverage_state: "COMPLETE_WITHIN_STATED_SCOPE", unknown_tokens: ["TIMEOUT"] }],
  132|       ["invented unknown token", { coverage_state: "PARTIAL", unknown_tokens: ["CLEAN"] }],
  133|       ["duplicate unknown token", { coverage_state: "PARTIAL", unknown_tokens: ["TIMEOUT", "TIMEOUT"] }],
  134|       ["effect escalation", { effect_ceiling: "E2_WRITE" }],
  135|       ["network escalation", { network_policy: "ALLOW_NETWORK" }],
  136|       ["egress escalation", { egress_policy: "ALLOW_EGRESS" }],
  137|       ["attempted verdict", { verdict: "PASS" }],
  138|       ["attempted severity", { severity: "critical" }],
  139|       ["self attestation", { finding_validated: true }],
  140|       ["secret material", { producer_id: "ghp_" + "x".repeat(36) }],
  141|     ];
  142|     for (const [name, change] of invalid) {
  143|       const outcome = validateSentrdelWorkflowInputV1(input(change));
  144|       expect(outcome.valid, name).toBe(false);
  145|       expect(outcome.reasons.length, name).toBeGreaterThan(0);
  146|       expect(() => normalizeSentrdelWorkflowObservationV1(input(change)), name).toThrow(TypeError);
  147|     }
  148|   });
  149| 
  150|   it("refuses accessor-driven identity changes at direct entry points", () => {
  151|     let getterCalls = 0;
  152|     const accessor = { ...input() };
  153|     Object.defineProperty(accessor, "source_head", {
  154|       enumerable: true,
  155|       get() {
  156|         getterCalls += 1;
  157|         return getterCalls < 2 ? "a".repeat(40) : "b".repeat(40);
  158|       },
  159|     });
  160|     expect(validateSentrdelWorkflowInputV1(accessor).valid).toBe(false);
  161|     expect(() => normalizeSentrdelWorkflowObservationV1(accessor)).toThrow(TypeError);
  162|     expect(getterCalls).toBe(0);
  163| 
  164|     const hidden = { ...input() };
  165|     Object.defineProperty(hidden, "assurance_override", { value: "PASS", enumerable: false });
  166|     const symbolic = { ...input(), [Symbol("authority")]: "SUPPORTED" };
  167|     const sparse = Array(1);
  168|     const nested = ["TIMEOUT"];
  169|     Object.defineProperty(nested, "0", { enumerable: true, get: () => "TIMEOUT" });
  170|     for (const candidate of [hidden, symbolic, input({ unknown_tokens: sparse }),
  171|       input({ unknown_tokens: nested })]) {
  172|       expect(validateSentrdelWorkflowInputV1(candidate).valid).toBe(false);
  173|       expect(() => normalizeSentrdelWorkflowObservationV1(candidate)).toThrow(TypeError);
  174|     }
  175|     expect(normalizeSentrdelWorkflowObservationV1(input()).authority)
  176|       .toBe("CONFIG_OBSERVATION_ONLY");
  177|   });
  178| 
  179|   it("uses the captured array length, so a Proxy cannot smuggle a hole past validation", () => {
  180|     // Keys 0 and 2 only. The `get` trap answers `length` with 2 on the read that
  181|     // compares the key count and 3 afterwards; any fresh read admits the hole.
  182|     const lyingTokens = () => {
  183|       const target: string[] = ["PARSER_UNSUPPORTED", "x", "TIMEOUT"];
  184|       delete (target as unknown as Record<string, unknown>)[1];
  185|       let reads = 0;
  186|       return new Proxy(target, {
  187|         get(t, key, receiver) {
  188|           if (key === "length") return ++reads === 2 ? 2 : 3;
  189|           return Reflect.get(t, key, receiver);
  190|         },
  191|       });
  192|     };
  193|     const candidate = input({ coverage_state: "PARTIAL", unknown_tokens: lyingTokens() });
  194|     expect(validateSentrdelWorkflowInputV1(candidate).valid).toBe(false);
  195|     expect(() => normalizeSentrdelWorkflowObservationV1(
  196|       input({ coverage_state: "PARTIAL", unknown_tokens: lyingTokens() }),
  197|     )).toThrow(TypeError);
  198|   });
  199| 
  200|   it("refuses malformed nonrecord input and unknown arrays", () => {
  201|     for (const value of [null, undefined, [], 1, "ready"]) {
  202|       expect(validateSentrdelWorkflowInputV1(value).valid).toBe(false);
  203|     }
  204|     for (const value of [null, "TIMEOUT", Array(9).fill("TIMEOUT")]) {
  205|       expect(validateSentrdelWorkflowInputV1(input({ unknown_tokens: value })).valid).toBe(false);
  206|     }
  207|   });
  208| });
```
