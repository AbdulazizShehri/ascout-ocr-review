You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: 0da75a0d0c5c07d3670d5808805e269caafacedd..7087ab2ec2fcadaeebea694ae42c1588aa5cf659 (this PR's own changes relative to its parent branch feat/ua-p06-t09b-config-presence)
Pull request title (context only): feat(security): UA-P06-T09C reject mixed-source inventory evidence
Changed files: src/assurance/security/sentrdel-t09-inventory.ts,tests/assurance-security-t09c.test.ts

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
- from: 0da75a0d0c5c07d3670d5808805e269caafacedd
- to: 7087ab2ec2fcadaeebea694ae42c1588aa5cf659
- merge_base: 0da75a0d0c5c07d3670d5808805e269caafacedd
- total_insertions: 357
- total_deletions: 0

  - `src/assurance/security/sentrdel-t09-inventory.ts` [added] +138/-0
~~- `tests/assurance-security-t09c.test.ts` [added] +219/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- src/assurance/security/sentrdel-t09-inventory.ts
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
diff --git a/src/assurance/security/sentrdel-t09-inventory.ts b/src/assurance/security/sentrdel-t09-inventory.ts
new file mode 100644
index 0000000..fe8de99
--- /dev/null
+++ b/src/assurance/security/sentrdel-t09-inventory.ts
@@ -0,0 +1,138 @@
+/**
+ * UA-P06-T09, grain C: fail-closed composition of untrusted static observations.
+ *
+ * This is not an engine runtime, security verdict, or evidence of scanner
+ * execution. It prevents cross-source/run evidence mixing.
+ */
+import { createHash } from "node:crypto";
+import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
+import {
+  buildSentrdelGenericIacGapV1,
+  normalizeSentrdelWorkflowObservationV1,
+  type SentrdelWorkflowObservationV1,
+} from "./sentrdel-workflow-normalization.js";
+import {
+  normalizeSentrdelConfigPresenceV1,
+  type SentrdelConfigPresenceObservationV1,
+} from "./sentrdel-config-presence.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "./sentrdel-source-pin.js";
+
+export const SENTRDEL_T09_INVENTORY_AUTHORITY = "UA-P06-T09" as const;
+export const SENTRDEL_T09_MAX_OBSERVATIONS = 64 as const;
+
+export interface SentrdelT09InventoryInputV1 {
+  readonly workflows: readonly unknown[];
+  readonly configurations: readonly unknown[];
+}
+
+export interface SentrdelT09InventoryV1 {
+  readonly schema_version: 1;
+  readonly phase_authority: typeof SENTRDEL_T09_INVENTORY_AUTHORITY;
+  readonly inventory_id: string;
+  readonly request_id: string;
+  readonly attempt_id: string;
+  readonly source_head: string;
+  readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
+  readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
+  readonly workflow_observations: readonly SentrdelWorkflowObservationV1[];
+  readonly config_presence_observations: readonly SentrdelConfigPresenceObservationV1[];
+  readonly generic_iac: ReturnType<typeof buildSentrdelGenericIacGapV1>;
+  readonly authority: "STATIC_OBSERVATION_INVENTORY_ONLY";
+  readonly assurance_effect: "NONE";
+  readonly executed_scanner_proven: false;
+  readonly coverage_proven_complete: false;
+  readonly repository_clean_claimed: false;
+  readonly findings_emitted: false;
+  readonly claim_assessment_emitted: false;
+}
+
+function strictInput(value: unknown): value is SentrdelT09InventoryInputV1 {
+  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
+  const data = value as Record<string, unknown>;
+  return Object.keys(data).length === 2
+    && Object.hasOwn(data, "workflows")
+    && Object.hasOwn(data, "configurations")
+    && Array.isArray(data["workflows"])
+    && Array.isArray(data["configurations"]);
+}
+
+/**
+ * Re-normalize RAW records at the boundary. Do not trust pre-built records,
+ * user-supplied execution states, or purported clean scan result.
+ */
+export function buildSentrdelT09InventoryV1(value: unknown): SentrdelT09InventoryV1 {
+  const stable = snapshotSentrdelObservationDataV1(value);
+  if (!strictInput(stable)) throw new TypeError("T09 inventory requires exact raw input arrays");
+  const { workflows, configurations } = stable;
+  if (workflows.length + configurations.length === 0) {
+    throw new TypeError("T09 inventory needs at least one observation; absence is NOT_RUN");
+  }
+  if (workflows.length + configurations.length > SENTRDEL_T09_MAX_OBSERVATIONS) {
+    throw new TypeError("T09 inventory observation limit exceeded");
+  }
+
+  const normalizedWorkflows = workflows.map(normalizeSentrdelWorkflowObservationV1);
+  const normalizedConfig = configurations.map(normalizeSentrdelConfigPresenceV1);
+  const all = [...normalizedWorkflows, ...normalizedConfig];
+  const [first] = all;
+  if (first === undefined) throw new TypeError("empty T09 inventory");
+  const { source_head, request_id, attempt_id, engine_pin, engine_tree } = first;
+  for (const record of all) {
+    if (record.source_head !== source_head ||
+        record.request_id !== request_id ||
+        record.attempt_id !== attempt_id ||
+        record.engine_pin !== engine_pin ||
+        record.engine_tree !== engine_tree) {
+      throw new TypeError("T09 inventory refuses cross-source, cross-attempt, or cross-pin observations");
+    }
+  }
+  // Records may share one evidence artifact, but never with different digests.
+  const digestByEvidenceRef = new Map<string, string>();
+  for (const { provenance } of all) {
+    const known = digestByEvidenceRef.get(provenance.evidence_ref);
+    if (known !== undefined && known !== provenance.evidence_digest) {
+      throw new TypeError("T09 inventory refuses one evidence reference with conflicting digests");
+    }
+    digestByEvidenceRef.set(provenance.evidence_ref, provenance.evidence_digest);
+  }
+  // UTF-16 code-unit ordering is deterministic across host locales/ICU versions.
+  // Never use localeCompare for identity-bearing or receipt-bearing canonical order.
+  const compareIdentity = (left: string, right: string): number =>
+    left < right ? -1 : left > right ? 1 : 0;
+  const sortedWorkflows = Object.freeze([...normalizedWorkflows].sort((a, b) =>
+    compareIdentity(a.observation_id, b.observation_id)));
+  const sortedConfig = Object.freeze([...normalizedConfig].sort((a, b) =>
+    compareIdentity(a.identity, b.identity)));
+
+  const allIds = [...sortedWorkflows.map(x => x.observation_id),
+    ...sortedConfig.map(x => x.identity)];
+  if (new Set(allIds).size !== allIds.length) {
+    throw new TypeError("T09 inventory rejects repeated evidence records");
+  }
+
+  const fingerprint = createHash("sha256").update(JSON.stringify([
+    SENTRDEL_T09_INVENTORY_AUTHORITY, request_id, attempt_id, source_head,
+    engine_pin, engine_tree, ...allIds,
+  ]), "utf8").digest("hex");
+
+  return Object.freeze({
+    schema_version: 1 as const,
+    phase_authority: SENTRDEL_T09_INVENTORY_AUTHORITY,
+    inventory_id: "t09-inventory:sentrdel:" + fingerprint,
+    request_id,
+    attempt_id,
+    source_head,
+    engine_pin,
+    engine_tree,
+    workflow_observations: sortedWorkflows,
+    config_presence_observations: sortedConfig,
+    generic_iac: buildSentrdelGenericIacGapV1(),
+    authority: "STATIC_OBSERVATION_INVENTORY_ONLY" as const,
+    assurance_effect: "NONE" as const,
+    executed_scanner_proven: false as const,
+    coverage_proven_complete: false as const,
+    repository_clean_claimed: false as const,
+    findings_emitted: false as const,
+    claim_assessment_emitted: false as const,
+  });
+}
diff --git a/tests/assurance-security-t09c.test.ts b/tests/assurance-security-t09c.test.ts
new file mode 100644
index 0000000..fe6ad45
--- /dev/null
+++ b/tests/assurance-security-t09c.test.ts
@@ -0,0 +1,219 @@
+import { describe, expect, it } from "vitest";
+import {
+  buildSentrdelT09InventoryV1,
+  SENTRDEL_T09_MAX_OBSERVATIONS,
+} from "../src/assurance/security/sentrdel-t09-inventory.js";
+import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
+
+const SHARED = {
+  schema_version: 1,
+  request_id: "request:test",
+  attempt_id: "attempt:test",
+  source_head: "a".repeat(40),
+  engine_id: SENTRDEL_ENGINE_ID,
+  engine_pin: SENTRDEL_PINNED_REVISION,
+  engine_tree: SENTRDEL_PINNED_TREE,
+  engine_version: SENTRDEL_ENGINE_VERSION,
+};
+
+function workflow(extra: Record<string, unknown> = {}) {
+  return {
+    ...SHARED, capability_id: "github-actions", execution_state: "EXECUTED",
+    rule_id: "gha.pull-request-target",
+    workflow_path: ".github/workflows/ci.yml",
+    line: 12,
+    producer_id: "producer:fixture", evidence_ref: "evidence:ci",
+    evidence_digest: "b".repeat(64),
+    coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
+    unknown_tokens: [],
+    effect_ceiling: "E0_READ_ONLY_ANALYSIS",
+    network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS", ...extra,
+  };
+}
+
+function configuration(extra: Record<string, unknown> = {}) {
+  return {
+    ...SHARED, capability_id: "config-inspection",
+    path: ".mcp.json", signal: "mcp-json",
+    producer_id: "producer:fixture", evidence_ref: "evidence:mcp",
+    evidence_digest: "c".repeat(64), ...extra,
+  };
+}
+
+describe("UA-P06-T09C source/attempt-bound static inventory", () => {
+  it("combines only same-source/same-attempt observations with no assurance promotion", () => {
+    const result = buildSentrdelT09InventoryV1({
+      workflows: [workflow()], configurations: [configuration()],
+    });
+    expect(result.phase_authority).toBe("UA-P06-T09");
+    expect(result.source_head).toBe(SHARED.source_head);
+    expect(result.engine_pin).toBe(SENTRDEL_PINNED_REVISION);
+    expect(result.generic_iac.status).toBe("NOT_RUN");
+    expect(result.generic_iac.clean_claimed).toBe(false);
+    expect(result.workflow_observations).toHaveLength(1);
+    expect(result.config_presence_observations).toHaveLength(1);
+    expect(result.assurance_effect).toBe("NONE");
+    expect(result.authority).toBe("STATIC_OBSERVATION_INVENTORY_ONLY");
+    expect(result.executed_scanner_proven).toBe(false);
+    expect(result.coverage_proven_complete).toBe(false);
+    expect(result.repository_clean_claimed).toBe(false);
+    expect(result.findings_emitted).toBe(false);
+    expect(result.claim_assessment_emitted).toBe(false);
+    expect(Object.isFrozen(result)).toBe(true);
+    expect(Object.isFrozen(result.workflow_observations)).toBe(true);
+    expect(Object.isFrozen(result.config_presence_observations)).toBe(true);
+    expect(JSON.stringify(result)).not.toMatch(/"PASS"|"SUPPORTED"/u);
+  });
+
+  it("sorts observation IDs and produces a stable order-independent inventory", () => {
+    const workflows = [workflow({ line: 45 }), workflow({ line: 12 })];
+    const configurations = [
+      configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
+      configuration(),
+    ];
+    const a = buildSentrdelT09InventoryV1({ workflows, configurations });
+    const b = buildSentrdelT09InventoryV1({
+      workflows: [...workflows].reverse(), configurations: [...configurations].reverse(),
+    });
+    expect(a).toEqual(b);
+    expect(a.inventory_id).toBe(b.inventory_id);
+    expect(a.workflow_observations[0]?.observation_id).not.toBe(a.workflow_observations[1]?.observation_id);
+    expect(a.config_presence_observations[0]?.identity).not.toBe(a.config_presence_observations[1]?.identity);
+  });
+
+  it("does not depend on localeCompare or host ICU collation for canonical IDs", () => {
+    const values = {
+      workflows: [workflow({ line: 45 }), workflow({ line: 12 })],
+      configurations: [
+        configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
+        configuration(),
+      ],
+    };
+    const expected = buildSentrdelT09InventoryV1(values);
+    const original = String.prototype.localeCompare;
+    try {
+      String.prototype.localeCompare = () => {
+        throw new Error("locale-specific sorting is forbidden in evidence identity");
+      };
+      const got = buildSentrdelT09InventoryV1({
+        workflows: [...values.workflows].reverse(),
+        configurations: [...values.configurations].reverse(),
+      });
+      expect(got.inventory_id).toBe(expected.inventory_id);
+      expect(got.workflow_observations.map(x => x.observation_id)).toEqual(
+        expected.workflow_observations.map(x => x.observation_id),
+      );
+      expect(got.config_presence_observations.map(x => x.identity)).toEqual(
+        expected.config_presence_observations.map(x => x.identity),
+      );
+    } finally {
+      String.prototype.localeCompare = original;
+    }
+  });
+
+  it("refuses cross-head and cross-attempt pooling for both record types", () => {
+    for (const patch of [
+      { source_head: "d".repeat(40) }, { request_id: "request:other" },
+      { attempt_id: "attempt:other" },
+    ]) {
+      expect(() => buildSentrdelT09InventoryV1({
+        workflows: [workflow()], configurations: [configuration(patch)],
+      })).toThrow(/cross-source/);
+      expect(() => buildSentrdelT09InventoryV1({
+        workflows: [workflow(patch)], configurations: [configuration()],
+      })).toThrow(/cross-source/);
+    }
+  });
+
+  it("refuses duplicate observations rather than inflating coverage", () => {
+    expect(() => buildSentrdelT09InventoryV1({
+      workflows: [workflow(), workflow()], configurations: [],
+    })).toThrow(/repeated evidence/);
+    expect(() => buildSentrdelT09InventoryV1({
+      workflows: [], configurations: [configuration(), configuration()],
+    })).toThrow(/repeated evidence/);
+  });
+
+  it("refuses one evidence reference bound to conflicting digests", () => {
+    const second = { rule_id: "gha.mutable-action-ref", line: 30 };
+    expect(() => buildSentrdelT09InventoryV1({
+      workflows: [workflow(), workflow({ ...second, evidence_digest: "d".repeat(64) })],
+      configurations: [],
+    })).toThrow(/conflicting digests/);
+    expect(() => buildSentrdelT09InventoryV1({
+      workflows: [workflow()],
+      configurations: [configuration({ evidence_ref: "evidence:ci" })],
+    })).toThrow(/conflicting digests/);
+    // Sharing one artifact with the same digest is legitimate.
+    const shared = buildSentrdelT09InventoryV1({
+      workflows: [workflow(), workflow(second)],
+      configurations: [configuration({ evidence_ref: "evidence:ci", evidence_digest: "b".repeat(64) })],
+    });
+    expect(shared.workflow_observations).toHaveLength(2);
+    expect(shared.config_presence_observations).toHaveLength(1);
+  });
+
+  it("refuses unverifiable, malformed, empty, and excessive raw inputs", () => {
+    const invalid: unknown[] = [
+      null, "PASS", [], {}, { workflows: [], configurations: [] },
+      { workflows: [], configurations: [], assessment: "PASS" },
+      { workflows: "fake", configurations: [] },
+      { workflows: [], configurations: 1 },
+      { workflows: [workflow({ rule_id: "gha.fake" })], configurations: [] },
+      { workflows: [], configurations: [configuration({ execution_state: "EXECUTED" })] },
+      { workflows: [], configurations: [configuration({ source_head: "bad" })] },
+      { workflows: [], configurations: [configuration({ path: "../secret" })] },
+      { workflows: Array(SENTRDEL_T09_MAX_OBSERVATIONS + 1).fill(workflow()),
+        configurations: [] },
+    ];
+    for (const value of invalid) {
+      expect(() => buildSentrdelT09InventoryV1(value)).toThrow(TypeError);
+    }
+  });
+
+  it("refuses accessor, hidden, symbol, and sparse input mutations", () => {
+    let observed = 0;
+    const getterRecord = { ...workflow() };
+    Object.defineProperty(getterRecord, "workflow_path", {
+      enumerable: true,
+      get() {
+        observed += 1;
+        return observed < 4 ? ".github/workflows/ci.yml" : "../unsafe.yml";
+      },
+    });
+    const hiddenRecord = { ...configuration() };
+    Object.defineProperty(hiddenRecord, "verdict", { value: "PASS", enumerable: false });
+    const symbolRecord = { ...configuration(), [Symbol("bypass")]: "PASS" };
+    const sparseRecords = Array(1);
+    const nestedAccessor = { ...workflow() };
+    const unknownTokens: string[] = ["TIMEOUT"];
+    Object.defineProperty(unknownTokens, "0", {
+      enumerable: true, get: () => "TIMEOUT",
+    });
+    nestedAccessor.unknown_tokens = unknownTokens;
+    for (const input of [
+      { workflows: [getterRecord], configurations: [] },
+      { workflows: [], configurations: [hiddenRecord] },
+      { workflows: [], configurations: [symbolRecord] },
+      { workflows: sparseRecords, configurations: [] },
+      { workflows: [nestedAccessor], configurations: [] },
+    ]) {
+      expect(() => buildSentrdelT09InventoryV1(input)).toThrow(TypeError);
+    }
+    expect(observed).toBe(0);
+  });
+
+  it("accepts a single characterized surface without inferring the absent one was checked", () => {
+    const a = buildSentrdelT09InventoryV1({ workflows: [workflow()], configurations: [] });
+    const b = buildSentrdelT09InventoryV1({ workflows: [], configurations: [configuration()] });
+    expect(a.workflow_observations).toHaveLength(1);
+    expect(a.config_presence_observations).toHaveLength(0);
+    expect(b.workflow_observations).toHaveLength(0);
+    expect(b.config_presence_observations).toHaveLength(1);
+    expect(a.coverage_proven_complete).toBe(false);
+    expect(b.coverage_proven_complete).toBe(false);
+    expect(a.generic_iac.status).toBe("NOT_RUN");
+    expect(b.generic_iac.status).toBe("NOT_RUN");
+  });
+});
```

## Full file at head: src/assurance/security/sentrdel-t09-inventory.ts
```
    1| /**
    2|  * UA-P06-T09, grain C: fail-closed composition of untrusted static observations.
    3|  *
    4|  * This is not an engine runtime, security verdict, or evidence of scanner
    5|  * execution. It prevents cross-source/run evidence mixing.
    6|  */
    7| import { createHash } from "node:crypto";
    8| import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
    9| import {
   10|   buildSentrdelGenericIacGapV1,
   11|   normalizeSentrdelWorkflowObservationV1,
   12|   type SentrdelWorkflowObservationV1,
   13| } from "./sentrdel-workflow-normalization.js";
   14| import {
   15|   normalizeSentrdelConfigPresenceV1,
   16|   type SentrdelConfigPresenceObservationV1,
   17| } from "./sentrdel-config-presence.js";
   18| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "./sentrdel-source-pin.js";
   19| 
   20| export const SENTRDEL_T09_INVENTORY_AUTHORITY = "UA-P06-T09" as const;
   21| export const SENTRDEL_T09_MAX_OBSERVATIONS = 64 as const;
   22| 
   23| export interface SentrdelT09InventoryInputV1 {
   24|   readonly workflows: readonly unknown[];
   25|   readonly configurations: readonly unknown[];
   26| }
   27| 
   28| export interface SentrdelT09InventoryV1 {
   29|   readonly schema_version: 1;
   30|   readonly phase_authority: typeof SENTRDEL_T09_INVENTORY_AUTHORITY;
   31|   readonly inventory_id: string;
   32|   readonly request_id: string;
   33|   readonly attempt_id: string;
   34|   readonly source_head: string;
   35|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   36|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   37|   readonly workflow_observations: readonly SentrdelWorkflowObservationV1[];
   38|   readonly config_presence_observations: readonly SentrdelConfigPresenceObservationV1[];
   39|   readonly generic_iac: ReturnType<typeof buildSentrdelGenericIacGapV1>;
   40|   readonly authority: "STATIC_OBSERVATION_INVENTORY_ONLY";
   41|   readonly assurance_effect: "NONE";
   42|   readonly executed_scanner_proven: false;
   43|   readonly coverage_proven_complete: false;
   44|   readonly repository_clean_claimed: false;
   45|   readonly findings_emitted: false;
   46|   readonly claim_assessment_emitted: false;
   47| }
   48| 
   49| function strictInput(value: unknown): value is SentrdelT09InventoryInputV1 {
   50|   if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
   51|   const data = value as Record<string, unknown>;
   52|   return Object.keys(data).length === 2
   53|     && Object.hasOwn(data, "workflows")
   54|     && Object.hasOwn(data, "configurations")
   55|     && Array.isArray(data["workflows"])
   56|     && Array.isArray(data["configurations"]);
   57| }
   58| 
   59| /**
   60|  * Re-normalize RAW records at the boundary. Do not trust pre-built records,
   61|  * user-supplied execution states, or purported clean scan result.
   62|  */
   63| export function buildSentrdelT09InventoryV1(value: unknown): SentrdelT09InventoryV1 {
   64|   const stable = snapshotSentrdelObservationDataV1(value);
   65|   if (!strictInput(stable)) throw new TypeError("T09 inventory requires exact raw input arrays");
   66|   const { workflows, configurations } = stable;
   67|   if (workflows.length + configurations.length === 0) {
   68|     throw new TypeError("T09 inventory needs at least one observation; absence is NOT_RUN");
   69|   }
   70|   if (workflows.length + configurations.length > SENTRDEL_T09_MAX_OBSERVATIONS) {
   71|     throw new TypeError("T09 inventory observation limit exceeded");
   72|   }
   73| 
   74|   const normalizedWorkflows = workflows.map(normalizeSentrdelWorkflowObservationV1);
   75|   const normalizedConfig = configurations.map(normalizeSentrdelConfigPresenceV1);
   76|   const all = [...normalizedWorkflows, ...normalizedConfig];
   77|   const [first] = all;
   78|   if (first === undefined) throw new TypeError("empty T09 inventory");
   79|   const { source_head, request_id, attempt_id, engine_pin, engine_tree } = first;
   80|   for (const record of all) {
   81|     if (record.source_head !== source_head ||
   82|         record.request_id !== request_id ||
   83|         record.attempt_id !== attempt_id ||
   84|         record.engine_pin !== engine_pin ||
   85|         record.engine_tree !== engine_tree) {
   86|       throw new TypeError("T09 inventory refuses cross-source, cross-attempt, or cross-pin observations");
   87|     }
   88|   }
   89|   // Records may share one evidence artifact, but never with different digests.
   90|   const digestByEvidenceRef = new Map<string, string>();
   91|   for (const { provenance } of all) {
   92|     const known = digestByEvidenceRef.get(provenance.evidence_ref);
   93|     if (known !== undefined && known !== provenance.evidence_digest) {
   94|       throw new TypeError("T09 inventory refuses one evidence reference with conflicting digests");
   95|     }
   96|     digestByEvidenceRef.set(provenance.evidence_ref, provenance.evidence_digest);
   97|   }
   98|   // UTF-16 code-unit ordering is deterministic across host locales/ICU versions.
   99|   // Never use localeCompare for identity-bearing or receipt-bearing canonical order.
  100|   const compareIdentity = (left: string, right: string): number =>
  101|     left < right ? -1 : left > right ? 1 : 0;
  102|   const sortedWorkflows = Object.freeze([...normalizedWorkflows].sort((a, b) =>
  103|     compareIdentity(a.observation_id, b.observation_id)));
  104|   const sortedConfig = Object.freeze([...normalizedConfig].sort((a, b) =>
  105|     compareIdentity(a.identity, b.identity)));
  106| 
  107|   const allIds = [...sortedWorkflows.map(x => x.observation_id),
  108|     ...sortedConfig.map(x => x.identity)];
  109|   if (new Set(allIds).size !== allIds.length) {
  110|     throw new TypeError("T09 inventory rejects repeated evidence records");
  111|   }
  112| 
  113|   const fingerprint = createHash("sha256").update(JSON.stringify([
  114|     SENTRDEL_T09_INVENTORY_AUTHORITY, request_id, attempt_id, source_head,
  115|     engine_pin, engine_tree, ...allIds,
  116|   ]), "utf8").digest("hex");
  117| 
  118|   return Object.freeze({
  119|     schema_version: 1 as const,
  120|     phase_authority: SENTRDEL_T09_INVENTORY_AUTHORITY,
  121|     inventory_id: "t09-inventory:sentrdel:" + fingerprint,
  122|     request_id,
  123|     attempt_id,
  124|     source_head,
  125|     engine_pin,
  126|     engine_tree,
  127|     workflow_observations: sortedWorkflows,
  128|     config_presence_observations: sortedConfig,
  129|     generic_iac: buildSentrdelGenericIacGapV1(),
  130|     authority: "STATIC_OBSERVATION_INVENTORY_ONLY" as const,
  131|     assurance_effect: "NONE" as const,
  132|     executed_scanner_proven: false as const,
  133|     coverage_proven_complete: false as const,
  134|     repository_clean_claimed: false as const,
  135|     findings_emitted: false as const,
  136|     claim_assessment_emitted: false as const,
  137|   });
  138| }
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
    8| 
    9| const SHARED = {
   10|   schema_version: 1,
   11|   request_id: "request:test",
   12|   attempt_id: "attempt:test",
   13|   source_head: "a".repeat(40),
   14|   engine_id: SENTRDEL_ENGINE_ID,
   15|   engine_pin: SENTRDEL_PINNED_REVISION,
   16|   engine_tree: SENTRDEL_PINNED_TREE,
   17|   engine_version: SENTRDEL_ENGINE_VERSION,
   18| };
   19| 
   20| function workflow(extra: Record<string, unknown> = {}) {
   21|   return {
   22|     ...SHARED, capability_id: "github-actions", execution_state: "EXECUTED",
   23|     rule_id: "gha.pull-request-target",
   24|     workflow_path: ".github/workflows/ci.yml",
   25|     line: 12,
   26|     producer_id: "producer:fixture", evidence_ref: "evidence:ci",
   27|     evidence_digest: "b".repeat(64),
   28|     coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
   29|     unknown_tokens: [],
   30|     effect_ceiling: "E0_READ_ONLY_ANALYSIS",
   31|     network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS", ...extra,
   32|   };
   33| }
   34| 
   35| function configuration(extra: Record<string, unknown> = {}) {
   36|   return {
   37|     ...SHARED, capability_id: "config-inspection",
   38|     path: ".mcp.json", signal: "mcp-json",
   39|     producer_id: "producer:fixture", evidence_ref: "evidence:mcp",
   40|     evidence_digest: "c".repeat(64), ...extra,
   41|   };
   42| }
   43| 
   44| describe("UA-P06-T09C source/attempt-bound static inventory", () => {
   45|   it("combines only same-source/same-attempt observations with no assurance promotion", () => {
   46|     const result = buildSentrdelT09InventoryV1({
   47|       workflows: [workflow()], configurations: [configuration()],
   48|     });
   49|     expect(result.phase_authority).toBe("UA-P06-T09");
   50|     expect(result.source_head).toBe(SHARED.source_head);
   51|     expect(result.engine_pin).toBe(SENTRDEL_PINNED_REVISION);
   52|     expect(result.generic_iac.status).toBe("NOT_RUN");
   53|     expect(result.generic_iac.clean_claimed).toBe(false);
   54|     expect(result.workflow_observations).toHaveLength(1);
   55|     expect(result.config_presence_observations).toHaveLength(1);
   56|     expect(result.assurance_effect).toBe("NONE");
   57|     expect(result.authority).toBe("STATIC_OBSERVATION_INVENTORY_ONLY");
   58|     expect(result.executed_scanner_proven).toBe(false);
   59|     expect(result.coverage_proven_complete).toBe(false);
   60|     expect(result.repository_clean_claimed).toBe(false);
   61|     expect(result.findings_emitted).toBe(false);
   62|     expect(result.claim_assessment_emitted).toBe(false);
   63|     expect(Object.isFrozen(result)).toBe(true);
   64|     expect(Object.isFrozen(result.workflow_observations)).toBe(true);
   65|     expect(Object.isFrozen(result.config_presence_observations)).toBe(true);
   66|     expect(JSON.stringify(result)).not.toMatch(/"PASS"|"SUPPORTED"/u);
   67|   });
   68| 
   69|   it("sorts observation IDs and produces a stable order-independent inventory", () => {
   70|     const workflows = [workflow({ line: 45 }), workflow({ line: 12 })];
   71|     const configurations = [
   72|       configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
   73|       configuration(),
   74|     ];
   75|     const a = buildSentrdelT09InventoryV1({ workflows, configurations });
   76|     const b = buildSentrdelT09InventoryV1({
   77|       workflows: [...workflows].reverse(), configurations: [...configurations].reverse(),
   78|     });
   79|     expect(a).toEqual(b);
   80|     expect(a.inventory_id).toBe(b.inventory_id);
   81|     expect(a.workflow_observations[0]?.observation_id).not.toBe(a.workflow_observations[1]?.observation_id);
   82|     expect(a.config_presence_observations[0]?.identity).not.toBe(a.config_presence_observations[1]?.identity);
   83|   });
   84| 
   85|   it("does not depend on localeCompare or host ICU collation for canonical IDs", () => {
   86|     const values = {
   87|       workflows: [workflow({ line: 45 }), workflow({ line: 12 })],
   88|       configurations: [
   89|         configuration({ path: ".cursor/mcp.json", signal: "cursor-mcp" }),
   90|         configuration(),
   91|       ],
   92|     };
   93|     const expected = buildSentrdelT09InventoryV1(values);
   94|     const original = String.prototype.localeCompare;
   95|     try {
   96|       String.prototype.localeCompare = () => {
   97|         throw new Error("locale-specific sorting is forbidden in evidence identity");
   98|       };
   99|       const got = buildSentrdelT09InventoryV1({
  100|         workflows: [...values.workflows].reverse(),
  101|         configurations: [...values.configurations].reverse(),
  102|       });
  103|       expect(got.inventory_id).toBe(expected.inventory_id);
  104|       expect(got.workflow_observations.map(x => x.observation_id)).toEqual(
  105|         expected.workflow_observations.map(x => x.observation_id),
  106|       );
  107|       expect(got.config_presence_observations.map(x => x.identity)).toEqual(
  108|         expected.config_presence_observations.map(x => x.identity),
  109|       );
  110|     } finally {
  111|       String.prototype.localeCompare = original;
  112|     }
  113|   });
  114| 
  115|   it("refuses cross-head and cross-attempt pooling for both record types", () => {
  116|     for (const patch of [
  117|       { source_head: "d".repeat(40) }, { request_id: "request:other" },
  118|       { attempt_id: "attempt:other" },
  119|     ]) {
  120|       expect(() => buildSentrdelT09InventoryV1({
  121|         workflows: [workflow()], configurations: [configuration(patch)],
  122|       })).toThrow(/cross-source/);
  123|       expect(() => buildSentrdelT09InventoryV1({
  124|         workflows: [workflow(patch)], configurations: [configuration()],
  125|       })).toThrow(/cross-source/);
  126|     }
  127|   });
  128| 
  129|   it("refuses duplicate observations rather than inflating coverage", () => {
  130|     expect(() => buildSentrdelT09InventoryV1({
  131|       workflows: [workflow(), workflow()], configurations: [],
  132|     })).toThrow(/repeated evidence/);
  133|     expect(() => buildSentrdelT09InventoryV1({
  134|       workflows: [], configurations: [configuration(), configuration()],
  135|     })).toThrow(/repeated evidence/);
  136|   });
  137| 
  138|   it("refuses one evidence reference bound to conflicting digests", () => {
  139|     const second = { rule_id: "gha.mutable-action-ref", line: 30 };
  140|     expect(() => buildSentrdelT09InventoryV1({
  141|       workflows: [workflow(), workflow({ ...second, evidence_digest: "d".repeat(64) })],
  142|       configurations: [],
  143|     })).toThrow(/conflicting digests/);
  144|     expect(() => buildSentrdelT09InventoryV1({
  145|       workflows: [workflow()],
  146|       configurations: [configuration({ evidence_ref: "evidence:ci" })],
  147|     })).toThrow(/conflicting digests/);
  148|     // Sharing one artifact with the same digest is legitimate.
  149|     const shared = buildSentrdelT09InventoryV1({
  150|       workflows: [workflow(), workflow(second)],
  151|       configurations: [configuration({ evidence_ref: "evidence:ci", evidence_digest: "b".repeat(64) })],
  152|     });
  153|     expect(shared.workflow_observations).toHaveLength(2);
  154|     expect(shared.config_presence_observations).toHaveLength(1);
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
