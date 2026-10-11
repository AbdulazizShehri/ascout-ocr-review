You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad..1b03e0e95bce03f2c3cf6f0db905ba1faa96fadb (this PR's own changes relative to its parent branch main)
Pull request title (context only): feat(security): UA-P06-T09A bounded GitHub Actions observation normalization
Changed files: src/assurance/security/sentrdel-workflow-normalization.ts,tests/assurance-security-t09a.test.ts

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
- from: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- to: 1b03e0e95bce03f2c3cf6f0db905ba1faa96fadb
- merge_base: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- total_insertions: 390
- total_deletions: 0

  - `src/assurance/security/sentrdel-workflow-normalization.ts` [added] +232/-0
~~- `tests/assurance-security-t09a.test.ts` [added] +158/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
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
diff --git a/src/assurance/security/sentrdel-workflow-normalization.ts b/src/assurance/security/sentrdel-workflow-normalization.ts
new file mode 100644
index 0000000..f30ae74
--- /dev/null
+++ b/src/assurance/security/sentrdel-workflow-normalization.ts
@@ -0,0 +1,232 @@
+/**
+ * UA-P06-T09, grain A — bounded GitHub Actions observation normalization.
+ *
+ * This module consumes untrusted records. It does not execute a scanner,
+ * interpret an action, validate a vulnerability, or issue assurance claims.
+ * The pinned producer supports a subset of changed GitHub Actions workflows;
+ * generic IaC remains unsupported and must be reported separately.
+ */
+import { createHash } from "node:crypto";
+import {
+  buildSentrdelCapabilitiesV1,
+  getSentrdelCapabilityV1,
+} from "./sentrdel-capability-characterization.js";
+import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "./sentrdel-engine-boundary.js";
+import { containsSecretMaterialV1, containsExternalAttestationV1 } from "./sentrdel-evidence-normalization.js";
+import { SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES } from "./sentrdel-engine-adapter.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE, SENTRDEL_PIN_REF } from "./sentrdel-source-pin.js";
+
+export const SENTRDEL_WORKFLOW_PHASE_AUTHORITY = "UA-P06-T09" as const;
+export const SENTRDEL_WORKFLOW_CAPABILITY_ID = "github-actions" as const;
+export const SENTRDEL_GENERIC_IAC_CAPABILITY_ID = "iac-generic" as const;
+
+/** Rule IDs observed in the exact pinned donor github_actions.rs implementation. */
+export const SENTRDEL_WORKFLOW_RULE_IDS = Object.freeze([
+  "gha.permission-widening",
+  "gha.oidc-id-token-write",
+  "gha.pull-request-target",
+  "gha.secret-in-untrusted-pr-path",
+  "gha.untrusted-expression-shell",
+  "gha.mutable-action-ref",
+  "gha.self-hosted-runner-change",
+  "gha.trust-sensitive-artifact-cache-handoff",
+] as const);
+
+const RULE_SET: ReadonlySet<string> = new Set(SENTRDEL_WORKFLOW_RULE_IDS);
+const CAPABILITIES = buildSentrdelCapabilitiesV1();
+const WORKFLOW = getSentrdelCapabilityV1(CAPABILITIES, "github-actions");
+const GENERIC_IAC = getSentrdelCapabilityV1(CAPABILITIES, "iac-generic");
+const UNKNOWN_SET = new Set<string>(WORKFLOW?.unknown_tokens ?? []);
+const SHA1 = /^[a-f0-9]{40}$/u;
+const SHA256 = /^[a-f0-9]{64}$/u;
+const ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
+const PATH = /^\.github\/workflows\/[A-Za-z0-9_.-]+\.ya?ml$/u;
+const KEYS = Object.freeze([
+  "schema_version", "request_id", "attempt_id", "source_head", "engine_id",
+  "engine_pin", "engine_tree", "engine_version", "capability_id", "execution_state",
+  "rule_id", "workflow_path", "line", "producer_id", "evidence_ref",
+  "evidence_digest", "coverage_state", "unknown_tokens",
+  "effect_ceiling", "network_policy", "egress_policy",
+] as const);
+
+export interface SentrdelWorkflowInputV1 {
+  readonly schema_version: 1;
+  readonly request_id: string;
+  readonly attempt_id: string;
+  readonly source_head: string;
+  readonly engine_id: typeof SENTRDEL_ENGINE_ID;
+  readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
+  readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
+  readonly engine_version: typeof SENTRDEL_ENGINE_VERSION;
+  readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
+  readonly execution_state: "EXECUTED";
+  readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
+  readonly workflow_path: string;
+  readonly line: number;
+  readonly producer_id: string;
+  readonly evidence_ref: string;
+  readonly evidence_digest: string;
+  readonly coverage_state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
+  readonly unknown_tokens: readonly string[];
+  readonly effect_ceiling: "E0_READ_ONLY_ANALYSIS";
+  readonly network_policy: "NO_NETWORK";
+  readonly egress_policy: "NO_EGRESS";
+}
+
+export interface SentrdelWorkflowObservationV1 {
+  readonly schema_version: 1;
+  readonly phase_authority: typeof SENTRDEL_WORKFLOW_PHASE_AUTHORITY;
+  readonly observation_id: string;
+  readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
+  readonly source_head: string;
+  readonly request_id: string;
+  readonly attempt_id: string;
+  readonly engine_id: typeof SENTRDEL_ENGINE_ID;
+  readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
+  readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
+  readonly engine_pin_ref: typeof SENTRDEL_PIN_REF;
+  readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
+  readonly workflow_path: string;
+  readonly line: number;
+  readonly provenance: Readonly<{ producer_id: string; evidence_ref: string; evidence_digest: string }>;
+  readonly coverage: Readonly<{
+    state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
+    unknown_tokens: readonly string[];
+    repository_total: false;
+    unscanned_is_clean: false;
+  }>;
+  readonly authority: "CONFIG_OBSERVATION_ONLY";
+  readonly assurance_effect: "NONE";
+  readonly finding_emitted: false;
+  readonly claim_assessment_emitted: false;
+  readonly producer_execution_attested: false;
+  readonly severity_derived: false;
+  readonly remediation_verified: false;
+}
+
+export interface SentrdelWorkflowValidationV1 {
+  readonly valid: boolean;
+  readonly reasons: readonly string[];
+}
+
+function record(value: unknown): value is Record<string, unknown> {
+  return typeof value === "object" && value !== null && !Array.isArray(value);
+}
+
+export function validateSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflowValidationV1 {
+  const reasons: string[] = [];
+  if (!record(input)) {
+    return { valid: false, reasons: Object.freeze(["input must be a record"]) };
+  }
+  const expected = new Set<string>(KEYS);
+  if (Object.keys(input).length !== KEYS.length ||
+      Object.keys(input).some((key) => !expected.has(key))) {
+    reasons.push("input keys must match the exact bounded schema");
+  }
+  const exact: Readonly<Record<string, unknown>> = {
+    schema_version: 1, engine_id: SENTRDEL_ENGINE_ID,
+    engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
+    engine_version: SENTRDEL_ENGINE_VERSION, capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID,
+    execution_state: "EXECUTED", effect_ceiling: "E0_READ_ONLY_ANALYSIS",
+    network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS",
+  };
+  for (const [key, expectedValue] of Object.entries(exact)) {
+    if (input[key] !== expectedValue) reasons.push(`${key} does not match the pinned boundary`);
+  }
+  for (const key of ["request_id", "attempt_id", "producer_id", "evidence_ref"]) {
+    if (typeof input[key] !== "string" || !ID.test(input[key])) reasons.push(`${key} is invalid`);
+  }
+  if (typeof input["source_head"] !== "string" || !SHA1.test(input["source_head"])) {
+    reasons.push("source_head must be a canonical Git SHA-1");
+  }
+  if (typeof input["evidence_digest"] !== "string" || !SHA256.test(input["evidence_digest"])) {
+    reasons.push("evidence_digest must be a SHA-256 digest");
+  }
+  if (!RULE_SET.has(input["rule_id"] as string)) reasons.push("rule_id is not present at the pinned donor");
+  if (typeof input["workflow_path"] !== "string" || !PATH.test(input["workflow_path"])) {
+    reasons.push("workflow_path must be a canonical changed GitHub Actions YAML path");
+  }
+  if (!Number.isSafeInteger(input["line"]) || (input["line"] as number) < 1 ||
+      (input["line"] as number) > 1_000_000) reasons.push("line must be a bounded positive integer");
+  if (input["coverage_state"] !== "COMPLETE_WITHIN_STATED_SCOPE" &&
+      input["coverage_state"] !== "PARTIAL") reasons.push("coverage_state must be executed-scope coverage");
+  const tokens = input["unknown_tokens"];
+  if (!Array.isArray(tokens) || tokens.length > 8 ||
+      tokens.some((item: unknown) => typeof item !== "string" || !UNKNOWN_SET.has(item)) ||
+      new Set(tokens).size !== tokens.length) {
+    reasons.push("unknown_tokens must be unique characterized tokens");
+  } else if (tokens.length > 0 && input["coverage_state"] !== "PARTIAL") {
+    reasons.push("unknown tokens cannot be reported as complete coverage");
+  } else if (tokens.length === 0 && input["coverage_state"] === "PARTIAL") {
+    reasons.push("partial coverage must declare its unknown reason");
+  }
+
+  if (WORKFLOW?.status !== "CHARACTERIZED" ||
+      !SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("github-actions")) {
+    reasons.push("pinned workflow capability is not characterized and adapter-admitted");
+  }
+  for (const value of Object.values(input)) {
+    if (typeof value === "string" &&
+        (containsSecretMaterialV1(value) || containsExternalAttestationV1(value))) {
+      reasons.push("untrusted strings may not contain secrets or self-attestation");
+      break;
+    }
+  }
+  return Object.freeze({ valid: reasons.length === 0, reasons: Object.freeze(reasons) });
+}
+
+/** This is data normalization, not a scan, review result, or proof of runtime execution. */
+export function normalizeSentrdelWorkflowObservationV1(
+  value: unknown,
+): SentrdelWorkflowObservationV1 {
+  const check = validateSentrdelWorkflowInputV1(value);
+  if (!check.valid) throw new TypeError(`invalid workflow observation: ${check.reasons.join("; ")}`);
+  const input = value as SentrdelWorkflowInputV1;
+  const unknown = Object.freeze([...input.unknown_tokens].sort());
+  const identity = [
+    SENTRDEL_WORKFLOW_PHASE_AUTHORITY, input.request_id, input.attempt_id,
+    input.engine_pin, input.engine_tree, input.engine_version,
+    input.source_head, input.rule_id, input.workflow_path,
+    String(input.line), input.producer_id, input.evidence_ref,
+    input.evidence_digest, input.coverage_state, ...unknown,
+  ];
+  const digest = createHash("sha256").update(JSON.stringify(identity), "utf8").digest("hex");
+  return Object.freeze({
+    schema_version: 1, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
+    observation_id: `ci-observation:sentrdel:${digest}`,
+    capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID, source_head: input.source_head,
+    request_id: input.request_id, attempt_id: input.attempt_id,
+    engine_id: SENTRDEL_ENGINE_ID, engine_pin: SENTRDEL_PINNED_REVISION,
+    engine_tree: SENTRDEL_PINNED_TREE, engine_pin_ref: SENTRDEL_PIN_REF,
+    rule_id: input.rule_id, workflow_path: input.workflow_path, line: input.line,
+    provenance: Object.freeze({
+      producer_id: input.producer_id, evidence_ref: input.evidence_ref,
+      evidence_digest: input.evidence_digest,
+    }),
+    coverage: Object.freeze({
+      state: input.coverage_state, unknown_tokens: unknown,
+      repository_total: false as const, unscanned_is_clean: false as const,
+    }),
+    authority: "CONFIG_OBSERVATION_ONLY" as const,
+    assurance_effect: "NONE" as const, finding_emitted: false as const,
+    claim_assessment_emitted: false as const, producer_execution_attested: false as const,
+    severity_derived: false as const, remediation_verified: false as const,
+  });
+}
+
+/** The pinned Sentrdel implementation has no generic IaC producer. */
+export function buildSentrdelGenericIacGapV1() {
+  if (GENERIC_IAC?.status !== "UNSUPPORTED" ||
+      SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("iac-generic")) {
+    throw new TypeError("pinned generic IaC characterization drifted");
+  }
+  return Object.freeze({
+    schema_version: 1 as const, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
+    capability_id: SENTRDEL_GENERIC_IAC_CAPABILITY_ID,
+    engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
+    status: "NOT_RUN" as const, reason_code: "unsupported_at_pinned_source" as const,
+    reason_text: "No generic IaC analyzer is implemented at the pinned Sentrdel revision.",
+    coverage_total: false as const, clean_claimed: false as const,
+    assurance_effect: "NONE" as const,
+  });
+}
diff --git a/tests/assurance-security-t09a.test.ts b/tests/assurance-security-t09a.test.ts
new file mode 100644
index 0000000..f656504
--- /dev/null
+++ b/tests/assurance-security-t09a.test.ts
@@ -0,0 +1,158 @@
+import { describe, expect, it } from "vitest";
+import {
+  SENTRDEL_WORKFLOW_RULE_IDS,
+  buildSentrdelGenericIacGapV1,
+  normalizeSentrdelWorkflowObservationV1,
+  validateSentrdelWorkflowInputV1,
+  type SentrdelWorkflowInputV1,
+} from "../src/assurance/security/sentrdel-workflow-normalization.js";
+import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
+
+const HEAD = "a".repeat(40);
+const DIGEST = "b".repeat(64);
+
+function input(overrides: Record<string, unknown> = {}): SentrdelWorkflowInputV1 {
+  return {
+    schema_version: 1,
+    request_id: "request:fixture",
+    attempt_id: "attempt:fixture",
+    source_head: HEAD,
+    engine_id: SENTRDEL_ENGINE_ID,
+    engine_pin: SENTRDEL_PINNED_REVISION,
+    engine_tree: SENTRDEL_PINNED_TREE,
+    engine_version: SENTRDEL_ENGINE_VERSION,
+    capability_id: "github-actions",
+    execution_state: "EXECUTED",
+    rule_id: "gha.pull-request-target",
+    workflow_path: ".github/workflows/ci.yml",
+    line: 17,
+    producer_id: "producer:sentrdel",
+    evidence_ref: "evidence:synthetic",
+    evidence_digest: DIGEST,
+    coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
+    unknown_tokens: [],
+    effect_ceiling: "E0_READ_ONLY_ANALYSIS",
+    network_policy: "NO_NETWORK",
+    egress_policy: "NO_EGRESS",
+    ...overrides,
+  } as SentrdelWorkflowInputV1;
+}
+
+describe("UA-P06-T09A bounded CI observation normalization", () => {
+  it("accepts each actual pinned GitHub Actions rule identifier", () => {
+    expect(SENTRDEL_WORKFLOW_RULE_IDS).toHaveLength(8);
+    for (const rule of SENTRDEL_WORKFLOW_RULE_IDS) {
+      const record = normalizeSentrdelWorkflowObservationV1(input({ rule_id: rule }));
+      expect(record.rule_id).toBe(rule);
+      expect(record.phase_authority).toBe("UA-P06-T09");
+      expect(record.authority).toBe("CONFIG_OBSERVATION_ONLY");
+      expect(record.assurance_effect).toBe("NONE");
+      expect(record.finding_emitted).toBe(false);
+      expect(record.claim_assessment_emitted).toBe(false);
+      expect(record.producer_execution_attested).toBe(false);
+      expect(record.severity_derived).toBe(false);
+      expect(record.remediation_verified).toBe(false);
+      expect(record.coverage.repository_total).toBe(false);
+      expect(record.coverage.unscanned_is_clean).toBe(false);
+      expect(JSON.stringify(record)).not.toMatch(/"PASS"|"SUPPORTED"|"CLEAN"/u);
+    }
+  });
+
+  it("is deterministic, frozen, and bound to exact source and evidence identity", () => {
+    const source = input();
+    const first = normalizeSentrdelWorkflowObservationV1(source);
+    expect(normalizeSentrdelWorkflowObservationV1(source)).toEqual(first);
+    expect(Object.isFrozen(first)).toBe(true);
+    expect(Object.isFrozen(first.provenance)).toBe(true);
+    expect(Object.isFrozen(first.coverage)).toBe(true);
+    expect(Object.isFrozen(first.coverage.unknown_tokens)).toBe(true);
+    expect(normalizeSentrdelWorkflowObservationV1(input({ source_head: "c".repeat(40) })).observation_id)
+      .not.toBe(first.observation_id);
+    expect(normalizeSentrdelWorkflowObservationV1(input({ evidence_digest: "d".repeat(64) })).observation_id)
+      .not.toBe(first.observation_id);
+    expect(normalizeSentrdelWorkflowObservationV1(input({ attempt_id: "attempt:other" })).observation_id)
+      .not.toBe(first.observation_id);
+    expect(normalizeSentrdelWorkflowObservationV1(input({ producer_id: "producer:other" })).observation_id)
+      .not.toBe(first.observation_id);
+    expect(normalizeSentrdelWorkflowObservationV1(input({ evidence_ref: "evidence:other" })).observation_id)
+      .not.toBe(first.observation_id);
+  });
+
+  it("preserves partial coverage and canonicalizes unknown reasons", () => {
+    const a = input({ coverage_state: "PARTIAL", unknown_tokens: ["TIMEOUT", "PARSER_UNSUPPORTED"] });
+    const b = input({ coverage_state: "PARTIAL", unknown_tokens: ["PARSER_UNSUPPORTED", "TIMEOUT"] });
+    const x = normalizeSentrdelWorkflowObservationV1(a);
+    expect(x).toEqual(normalizeSentrdelWorkflowObservationV1(b));
+    expect(x.coverage.unknown_tokens).toEqual(["PARSER_UNSUPPORTED", "TIMEOUT"]);
+    expect(x.coverage.state).toBe("PARTIAL");
+    expect(x.coverage.repository_total).toBe(false);
+  });
+
+  it("never promotes generic IaC absence into clean/supported scope", () => {
+    const gap = buildSentrdelGenericIacGapV1();
+    expect(gap.capability_id).toBe("iac-generic");
+    expect(gap.phase_authority).toBe("UA-P06-T09");
+    expect(gap.status).toBe("NOT_RUN");
+    expect(gap.reason_code).toBe("unsupported_at_pinned_source");
+    expect(gap.coverage_total).toBe(false);
+    expect(gap.clean_claimed).toBe(false);
+    expect(gap.assurance_effect).toBe("NONE");
+    expect(Object.isFrozen(gap)).toBe(true);
+    expect(buildSentrdelGenericIacGapV1()).toEqual(gap);
+  });
+
+  it("refuses unqualified and escalation-bearing observation input", () => {
+    const invalid: Array<[string, Record<string, unknown>]> = [
+      ["engine pin", { engine_pin: "0".repeat(40) }],
+      ["engine tree", { engine_tree: "0".repeat(40) }],
+      ["engine identity", { engine_id: "engine:other" }],
+      ["version", { engine_version: "99.0.0" }],
+      ["capability", { capability_id: "iac-generic" }],
+      ["unsupported CI format", { capability_id: "jenkins" }],
+      ["absent engine", { execution_state: "UNAVAILABLE" }],
+      ["timeout", { execution_state: "TIMEOUT" }],
+      ["engine error", { execution_state: "ENGINE_ERROR" }],
+      ["invented rule", { rule_id: "gha.does-not-exist" }],
+      ["absolute path", { workflow_path: "C:/private/workflow.yml" }],
+      ["parent traversal", { workflow_path: ".github/workflows/../ci.yml" }],
+      ["arbitrary YAML", { workflow_path: "config/ci.yml" }],
+      ["nested workflow path", { workflow_path: ".github/workflows/tmp/ci.yml" }],
+      ["unsafe path", { workflow_path: ".github/workflows/ci ; echo unsafe.yml" }],
+      ["invalid line", { line: 0 }],
+      ["noninteger line", { line: 1.5 }],
+      ["overflow line", { line: 1_000_001 }],
+      ["missing provenance", { producer_id: "" }],
+      ["missing evidence", { evidence_ref: "" }],
+      ["bad evidence digest", { evidence_digest: "123" }],
+      ["invalid head", { source_head: "123" }],
+      ["fabricated coverage", { coverage_state: "TOTAL" }],
+      ["unexplained partial", { coverage_state: "PARTIAL", unknown_tokens: [] }],
+      ["unknown in complete", { coverage_state: "COMPLETE_WITHIN_STATED_SCOPE", unknown_tokens: ["TIMEOUT"] }],
+      ["invented unknown token", { coverage_state: "PARTIAL", unknown_tokens: ["CLEAN"] }],
+      ["duplicate unknown token", { coverage_state: "PARTIAL", unknown_tokens: ["TIMEOUT", "TIMEOUT"] }],
+      ["effect escalation", { effect_ceiling: "E2_WRITE" }],
+      ["network escalation", { network_policy: "ALLOW_NETWORK" }],
+      ["egress escalation", { egress_policy: "ALLOW_EGRESS" }],
+      ["attempted verdict", { verdict: "PASS" }],
+      ["attempted severity", { severity: "critical" }],
+      ["self attestation", { finding_validated: true }],
+      ["secret material", { producer_id: "ghp_" + "x".repeat(36) }],
+    ];
+    for (const [name, change] of invalid) {
+      const outcome = validateSentrdelWorkflowInputV1(input(change));
+      expect(outcome.valid, name).toBe(false);
+      expect(outcome.reasons.length, name).toBeGreaterThan(0);
+      expect(() => normalizeSentrdelWorkflowObservationV1(input(change)), name).toThrow(TypeError);
+    }
+  });
+
+  it("refuses malformed nonrecord input and unknown arrays", () => {
+    for (const value of [null, undefined, [], 1, "ready"]) {
+      expect(validateSentrdelWorkflowInputV1(value).valid).toBe(false);
+    }
+    for (const value of [null, "TIMEOUT", Array(9).fill("TIMEOUT")]) {
+      expect(validateSentrdelWorkflowInputV1(input({ unknown_tokens: value })).valid).toBe(false);
+    }
+  });
+});
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
   10| import {
   11|   buildSentrdelCapabilitiesV1,
   12|   getSentrdelCapabilityV1,
   13| } from "./sentrdel-capability-characterization.js";
   14| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "./sentrdel-engine-boundary.js";
   15| import { containsSecretMaterialV1, containsExternalAttestationV1 } from "./sentrdel-evidence-normalization.js";
   16| import { SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES } from "./sentrdel-engine-adapter.js";
   17| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE, SENTRDEL_PIN_REF } from "./sentrdel-source-pin.js";
   18| 
   19| export const SENTRDEL_WORKFLOW_PHASE_AUTHORITY = "UA-P06-T09" as const;
   20| export const SENTRDEL_WORKFLOW_CAPABILITY_ID = "github-actions" as const;
   21| export const SENTRDEL_GENERIC_IAC_CAPABILITY_ID = "iac-generic" as const;
   22| 
   23| /** Rule IDs observed in the exact pinned donor github_actions.rs implementation. */
   24| export const SENTRDEL_WORKFLOW_RULE_IDS = Object.freeze([
   25|   "gha.permission-widening",
   26|   "gha.oidc-id-token-write",
   27|   "gha.pull-request-target",
   28|   "gha.secret-in-untrusted-pr-path",
   29|   "gha.untrusted-expression-shell",
   30|   "gha.mutable-action-ref",
   31|   "gha.self-hosted-runner-change",
   32|   "gha.trust-sensitive-artifact-cache-handoff",
   33| ] as const);
   34| 
   35| const RULE_SET: ReadonlySet<string> = new Set(SENTRDEL_WORKFLOW_RULE_IDS);
   36| const CAPABILITIES = buildSentrdelCapabilitiesV1();
   37| const WORKFLOW = getSentrdelCapabilityV1(CAPABILITIES, "github-actions");
   38| const GENERIC_IAC = getSentrdelCapabilityV1(CAPABILITIES, "iac-generic");
   39| const UNKNOWN_SET = new Set<string>(WORKFLOW?.unknown_tokens ?? []);
   40| const SHA1 = /^[a-f0-9]{40}$/u;
   41| const SHA256 = /^[a-f0-9]{64}$/u;
   42| const ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
   43| const PATH = /^\.github\/workflows\/[A-Za-z0-9_.-]+\.ya?ml$/u;
   44| const KEYS = Object.freeze([
   45|   "schema_version", "request_id", "attempt_id", "source_head", "engine_id",
   46|   "engine_pin", "engine_tree", "engine_version", "capability_id", "execution_state",
   47|   "rule_id", "workflow_path", "line", "producer_id", "evidence_ref",
   48|   "evidence_digest", "coverage_state", "unknown_tokens",
   49|   "effect_ceiling", "network_policy", "egress_policy",
   50| ] as const);
   51| 
   52| export interface SentrdelWorkflowInputV1 {
   53|   readonly schema_version: 1;
   54|   readonly request_id: string;
   55|   readonly attempt_id: string;
   56|   readonly source_head: string;
   57|   readonly engine_id: typeof SENTRDEL_ENGINE_ID;
   58|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   59|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   60|   readonly engine_version: typeof SENTRDEL_ENGINE_VERSION;
   61|   readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
   62|   readonly execution_state: "EXECUTED";
   63|   readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
   64|   readonly workflow_path: string;
   65|   readonly line: number;
   66|   readonly producer_id: string;
   67|   readonly evidence_ref: string;
   68|   readonly evidence_digest: string;
   69|   readonly coverage_state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
   70|   readonly unknown_tokens: readonly string[];
   71|   readonly effect_ceiling: "E0_READ_ONLY_ANALYSIS";
   72|   readonly network_policy: "NO_NETWORK";
   73|   readonly egress_policy: "NO_EGRESS";
   74| }
   75| 
   76| export interface SentrdelWorkflowObservationV1 {
   77|   readonly schema_version: 1;
   78|   readonly phase_authority: typeof SENTRDEL_WORKFLOW_PHASE_AUTHORITY;
   79|   readonly observation_id: string;
   80|   readonly capability_id: typeof SENTRDEL_WORKFLOW_CAPABILITY_ID;
   81|   readonly source_head: string;
   82|   readonly request_id: string;
   83|   readonly attempt_id: string;
   84|   readonly engine_id: typeof SENTRDEL_ENGINE_ID;
   85|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   86|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   87|   readonly engine_pin_ref: typeof SENTRDEL_PIN_REF;
   88|   readonly rule_id: (typeof SENTRDEL_WORKFLOW_RULE_IDS)[number];
   89|   readonly workflow_path: string;
   90|   readonly line: number;
   91|   readonly provenance: Readonly<{ producer_id: string; evidence_ref: string; evidence_digest: string }>;
   92|   readonly coverage: Readonly<{
   93|     state: "COMPLETE_WITHIN_STATED_SCOPE" | "PARTIAL";
   94|     unknown_tokens: readonly string[];
   95|     repository_total: false;
   96|     unscanned_is_clean: false;
   97|   }>;
   98|   readonly authority: "CONFIG_OBSERVATION_ONLY";
   99|   readonly assurance_effect: "NONE";
  100|   readonly finding_emitted: false;
  101|   readonly claim_assessment_emitted: false;
  102|   readonly producer_execution_attested: false;
  103|   readonly severity_derived: false;
  104|   readonly remediation_verified: false;
  105| }
  106| 
  107| export interface SentrdelWorkflowValidationV1 {
  108|   readonly valid: boolean;
  109|   readonly reasons: readonly string[];
  110| }
  111| 
  112| function record(value: unknown): value is Record<string, unknown> {
  113|   return typeof value === "object" && value !== null && !Array.isArray(value);
  114| }
  115| 
  116| export function validateSentrdelWorkflowInputV1(input: unknown): SentrdelWorkflowValidationV1 {
  117|   const reasons: string[] = [];
  118|   if (!record(input)) {
  119|     return { valid: false, reasons: Object.freeze(["input must be a record"]) };
  120|   }
  121|   const expected = new Set<string>(KEYS);
  122|   if (Object.keys(input).length !== KEYS.length ||
  123|       Object.keys(input).some((key) => !expected.has(key))) {
  124|     reasons.push("input keys must match the exact bounded schema");
  125|   }
  126|   const exact: Readonly<Record<string, unknown>> = {
  127|     schema_version: 1, engine_id: SENTRDEL_ENGINE_ID,
  128|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
  129|     engine_version: SENTRDEL_ENGINE_VERSION, capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID,
  130|     execution_state: "EXECUTED", effect_ceiling: "E0_READ_ONLY_ANALYSIS",
  131|     network_policy: "NO_NETWORK", egress_policy: "NO_EGRESS",
  132|   };
  133|   for (const [key, expectedValue] of Object.entries(exact)) {
  134|     if (input[key] !== expectedValue) reasons.push(`${key} does not match the pinned boundary`);
  135|   }
  136|   for (const key of ["request_id", "attempt_id", "producer_id", "evidence_ref"]) {
  137|     if (typeof input[key] !== "string" || !ID.test(input[key])) reasons.push(`${key} is invalid`);
  138|   }
  139|   if (typeof input["source_head"] !== "string" || !SHA1.test(input["source_head"])) {
  140|     reasons.push("source_head must be a canonical Git SHA-1");
  141|   }
  142|   if (typeof input["evidence_digest"] !== "string" || !SHA256.test(input["evidence_digest"])) {
  143|     reasons.push("evidence_digest must be a SHA-256 digest");
  144|   }
  145|   if (!RULE_SET.has(input["rule_id"] as string)) reasons.push("rule_id is not present at the pinned donor");
  146|   if (typeof input["workflow_path"] !== "string" || !PATH.test(input["workflow_path"])) {
  147|     reasons.push("workflow_path must be a canonical changed GitHub Actions YAML path");
  148|   }
  149|   if (!Number.isSafeInteger(input["line"]) || (input["line"] as number) < 1 ||
  150|       (input["line"] as number) > 1_000_000) reasons.push("line must be a bounded positive integer");
  151|   if (input["coverage_state"] !== "COMPLETE_WITHIN_STATED_SCOPE" &&
  152|       input["coverage_state"] !== "PARTIAL") reasons.push("coverage_state must be executed-scope coverage");
  153|   const tokens = input["unknown_tokens"];
  154|   if (!Array.isArray(tokens) || tokens.length > 8 ||
  155|       tokens.some((item: unknown) => typeof item !== "string" || !UNKNOWN_SET.has(item)) ||
  156|       new Set(tokens).size !== tokens.length) {
  157|     reasons.push("unknown_tokens must be unique characterized tokens");
  158|   } else if (tokens.length > 0 && input["coverage_state"] !== "PARTIAL") {
  159|     reasons.push("unknown tokens cannot be reported as complete coverage");
  160|   } else if (tokens.length === 0 && input["coverage_state"] === "PARTIAL") {
  161|     reasons.push("partial coverage must declare its unknown reason");
  162|   }
  163| 
  164|   if (WORKFLOW?.status !== "CHARACTERIZED" ||
  165|       !SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("github-actions")) {
  166|     reasons.push("pinned workflow capability is not characterized and adapter-admitted");
  167|   }
  168|   for (const value of Object.values(input)) {
  169|     if (typeof value === "string" &&
  170|         (containsSecretMaterialV1(value) || containsExternalAttestationV1(value))) {
  171|       reasons.push("untrusted strings may not contain secrets or self-attestation");
  172|       break;
  173|     }
  174|   }
  175|   return Object.freeze({ valid: reasons.length === 0, reasons: Object.freeze(reasons) });
  176| }
  177| 
  178| /** This is data normalization, not a scan, review result, or proof of runtime execution. */
  179| export function normalizeSentrdelWorkflowObservationV1(
  180|   value: unknown,
  181| ): SentrdelWorkflowObservationV1 {
  182|   const check = validateSentrdelWorkflowInputV1(value);
  183|   if (!check.valid) throw new TypeError(`invalid workflow observation: ${check.reasons.join("; ")}`);
  184|   const input = value as SentrdelWorkflowInputV1;
  185|   const unknown = Object.freeze([...input.unknown_tokens].sort());
  186|   const identity = [
  187|     SENTRDEL_WORKFLOW_PHASE_AUTHORITY, input.request_id, input.attempt_id,
  188|     input.engine_pin, input.engine_tree, input.engine_version,
  189|     input.source_head, input.rule_id, input.workflow_path,
  190|     String(input.line), input.producer_id, input.evidence_ref,
  191|     input.evidence_digest, input.coverage_state, ...unknown,
  192|   ];
  193|   const digest = createHash("sha256").update(JSON.stringify(identity), "utf8").digest("hex");
  194|   return Object.freeze({
  195|     schema_version: 1, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
  196|     observation_id: `ci-observation:sentrdel:${digest}`,
  197|     capability_id: SENTRDEL_WORKFLOW_CAPABILITY_ID, source_head: input.source_head,
  198|     request_id: input.request_id, attempt_id: input.attempt_id,
  199|     engine_id: SENTRDEL_ENGINE_ID, engine_pin: SENTRDEL_PINNED_REVISION,
  200|     engine_tree: SENTRDEL_PINNED_TREE, engine_pin_ref: SENTRDEL_PIN_REF,
  201|     rule_id: input.rule_id, workflow_path: input.workflow_path, line: input.line,
  202|     provenance: Object.freeze({
  203|       producer_id: input.producer_id, evidence_ref: input.evidence_ref,
  204|       evidence_digest: input.evidence_digest,
  205|     }),
  206|     coverage: Object.freeze({
  207|       state: input.coverage_state, unknown_tokens: unknown,
  208|       repository_total: false as const, unscanned_is_clean: false as const,
  209|     }),
  210|     authority: "CONFIG_OBSERVATION_ONLY" as const,
  211|     assurance_effect: "NONE" as const, finding_emitted: false as const,
  212|     claim_assessment_emitted: false as const, producer_execution_attested: false as const,
  213|     severity_derived: false as const, remediation_verified: false as const,
  214|   });
  215| }
  216| 
  217| /** The pinned Sentrdel implementation has no generic IaC producer. */
  218| export function buildSentrdelGenericIacGapV1() {
  219|   if (GENERIC_IAC?.status !== "UNSUPPORTED" ||
  220|       SENTRDEL_ADAPTER_ALLOWED_CAPABILITIES.includes("iac-generic")) {
  221|     throw new TypeError("pinned generic IaC characterization drifted");
  222|   }
  223|   return Object.freeze({
  224|     schema_version: 1 as const, phase_authority: SENTRDEL_WORKFLOW_PHASE_AUTHORITY,
  225|     capability_id: SENTRDEL_GENERIC_IAC_CAPABILITY_ID,
  226|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
  227|     status: "NOT_RUN" as const, reason_code: "unsupported_at_pinned_source" as const,
  228|     reason_text: "No generic IaC analyzer is implemented at the pinned Sentrdel revision.",
  229|     coverage_total: false as const, clean_claimed: false as const,
  230|     assurance_effect: "NONE" as const,
  231|   });
  232| }
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
  150|   it("refuses malformed nonrecord input and unknown arrays", () => {
  151|     for (const value of [null, undefined, [], 1, "ready"]) {
  152|       expect(validateSentrdelWorkflowInputV1(value).valid).toBe(false);
  153|     }
  154|     for (const value of [null, "TIMEOUT", Array(9).fill("TIMEOUT")]) {
  155|       expect(validateSentrdelWorkflowInputV1(input({ unknown_tokens: value })).valid).toBe(false);
  156|     }
  157|   });
  158| });
```
