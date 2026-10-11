You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: 5de4829ed1442b42ab812684b211c4dcebbaf8b3..0da75a0d0c5c07d3670d5808805e269caafacedd (this PR's own changes relative to its parent branch fix/ua-p06-t09-dataproperty-snapshot)
Pull request title (context only): feat(security): UA-P06-T09B pinned CI/MCP/Supabase presence normalization
Changed files: src/assurance/security/sentrdel-config-presence.ts,tests/assurance-security-t09b.test.ts

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
- from: 5de4829ed1442b42ab812684b211c4dcebbaf8b3
- to: 0da75a0d0c5c07d3670d5808805e269caafacedd
- merge_base: 5de4829ed1442b42ab812684b211c4dcebbaf8b3
- total_insertions: 359
- total_deletions: 0

  - `src/assurance/security/sentrdel-config-presence.ts` [added] +215/-0
~~- `tests/assurance-security-t09b.test.ts` [added] +144/-0 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- src/assurance/security/sentrdel-config-presence.ts
- tests/assurance-security-t09b.test.ts

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
diff --git a/src/assurance/security/sentrdel-config-presence.ts b/src/assurance/security/sentrdel-config-presence.ts
new file mode 100644
index 0000000..0369e78
--- /dev/null
+++ b/src/assurance/security/sentrdel-config-presence.ts
@@ -0,0 +1,215 @@
+/**
+ * UA-P06-T09, grain B: evidence-bound static CI/MCP/Supabase presence.
+ *
+ * Exact source: pinned Sentrdel config_detection.rs. This is inventory data
+ * only. No config contents, dynamic workflow, CI execution, credentials,
+ * remote MCP service, or hosted security posture are inspected.
+ */
+import { createHash } from "node:crypto";
+import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
+import {
+  buildSentrdelCapabilitiesV1,
+  getSentrdelCapabilityV1,
+} from "./sentrdel-capability-characterization.js";
+import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "./sentrdel-engine-boundary.js";
+import { containsSecretMaterialV1, containsExternalAttestationV1 } from "./sentrdel-evidence-normalization.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE, SENTRDEL_PIN_REF } from "./sentrdel-source-pin.js";
+
+export const SENTRDEL_CONFIG_PRESENCE_AUTHORITY = "UA-P06-T09" as const;
+export const SENTRDEL_CONFIG_PRESENCE_CAPABILITY = "config-inspection" as const;
+export const SENTRDEL_CONFIG_PRESENCE_SIGNALS = [
+  "github-actions", "gitlab-ci", "azure-pipelines", "jenkins", "circleci",
+  "mcp-json", "cursor-mcp", "vscode-mcp", "claude-mcp",
+  "supabase-config", "supabase-seed", "supabase-migration", "supabase-function",
+] as const;
+export type SentrdelPresenceSignalV1 = (typeof SENTRDEL_CONFIG_PRESENCE_SIGNALS)[number];
+const SIGNAL_SET = new Set<string>(SENTRDEL_CONFIG_PRESENCE_SIGNALS);
+const CAPABILITY = getSentrdelCapabilityV1(buildSentrdelCapabilitiesV1(), "config-inspection");
+const SHA1 = /^[0-9a-f]{40}$/u;
+const SHA256 = /^[0-9a-f]{64}$/u;
+const ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
+const PATH = /^[A-Za-z0-9._/-]{1,4096}$/u;
+const EXACT_KEYS = [
+  "schema_version", "request_id", "attempt_id", "source_head", "engine_id",
+  "engine_pin", "engine_tree", "engine_version", "capability_id",
+  "path", "signal", "producer_id", "evidence_ref", "evidence_digest",
+] as const;
+
+export interface SentrdelConfigPresenceInputV1 {
+  readonly schema_version: 1;
+  readonly request_id: string;
+  readonly attempt_id: string;
+  readonly source_head: string;
+  readonly engine_id: typeof SENTRDEL_ENGINE_ID;
+  readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
+  readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
+  readonly engine_version: typeof SENTRDEL_ENGINE_VERSION;
+  readonly capability_id: typeof SENTRDEL_CONFIG_PRESENCE_CAPABILITY;
+  readonly path: string;
+  readonly signal: SentrdelPresenceSignalV1;
+  readonly producer_id: string;
+  readonly evidence_ref: string;
+  readonly evidence_digest: string;
+}
+
+export interface SentrdelConfigPresenceObservationV1 {
+  readonly schema_version: 1;
+  readonly phase_authority: typeof SENTRDEL_CONFIG_PRESENCE_AUTHORITY;
+  readonly identity: string;
+  readonly source_head: string;
+  readonly request_id: string;
+  readonly attempt_id: string;
+  readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
+  readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
+  readonly pin_ref: typeof SENTRDEL_PIN_REF;
+  readonly capability_id: typeof SENTRDEL_CONFIG_PRESENCE_CAPABILITY;
+  readonly path: string;
+  readonly signal: SentrdelPresenceSignalV1;
+  readonly provenance: Readonly<{ producer_id: string; evidence_ref: string; evidence_digest: string }>;
+  readonly authority: "STATIC_PRESENCE_ONLY";
+  readonly assurance_effect: "NONE";
+  readonly producer_execution_attested: false;
+  readonly security_rule_executed: false;
+  readonly configuration_contents_scanned: false;
+  readonly ci_security_scanned: false;
+  readonly hosted_posture_verified: false;
+  readonly repository_total: false;
+  readonly finding_emitted: false;
+  readonly claim_assessment_emitted: false;
+}
+
+function isRecord(value: unknown): value is Record<string, unknown> {
+  return typeof value === "object" && value !== null && !Array.isArray(value);
+}
+
+/**
+ * Transcribes the pinned path-only producer classification. A recognized CI
+ * filename is not evidence that any of its instructions were evaluated.
+ */
+export function classifySentrdelConfigPresencePathV1(path: string): readonly SentrdelPresenceSignalV1[] {
+  if (!PATH.test(path) || path.startsWith("/") || path.endsWith("/") ||
+      path.split("/").some(part => part === "" || part === "." || part === "..")) {
+    return Object.freeze([]);
+  }
+  const base = path.slice(path.lastIndexOf("/") + 1);
+  const signals: SentrdelPresenceSignalV1[] = [];
+  if (path.startsWith(".github/workflows/") && /\.ya?ml$/u.test(path)) signals.push("github-actions");
+  if (base === ".gitlab-ci.yml" || base === ".gitlab-ci.yaml") signals.push("gitlab-ci");
+  if (base === "azure-pipelines.yml" || base === "azure-pipelines.yaml") signals.push("azure-pipelines");
+  if (base === "Jenkinsfile") signals.push("jenkins");
+  if (path.startsWith(".circleci/") && ["CircleCI.yml", "CircleCI.yaml", "config.yml", "config.yaml"].includes(base)) signals.push("circleci");
+  if (path === ".mcp.json" || path === "mcp.json") signals.push("mcp-json");
+  if (path === ".cursor/mcp.json") signals.push("cursor-mcp");
+  if (path === ".vscode/mcp.json") signals.push("vscode-mcp");
+  if (path.startsWith(".claude/") && base === "mcp.json") signals.push("claude-mcp");
+  // Pinned supabase_detection.rs recognizes local path layout, not live posture.
+  if (path === "supabase/config.toml") signals.push("supabase-config");
+  if (path === "supabase/seed.sql") signals.push("supabase-seed");
+  if (path.startsWith("supabase/migrations/")) {
+    const relative = path.slice("supabase/migrations/".length);
+    if (relative.length > 0 && !relative.includes("/") && relative.endsWith(".sql")) {
+      signals.push("supabase-migration");
+    }
+  }
+  if (path.startsWith("supabase/functions/")) {
+    const parts = path.slice("supabase/functions/".length).split("/");
+    if (parts.length >= 2 && parts[0]!.length > 0 && parts[1]!.length > 0) {
+      signals.push("supabase-function");
+    }
+  }
+  return Object.freeze(signals);
+}
+
+function validatePlainSentrdelConfigPresenceInputV1(value: unknown): readonly string[] {
+  const reasons: string[] = [];
+  if (!isRecord(value)) return Object.freeze(["input must be a record"]);
+  if (Object.keys(value).length !== EXACT_KEYS.length ||
+      Object.keys(value).some(key => !(EXACT_KEYS as readonly string[]).includes(key))) {
+    reasons.push("input keys must exactly match schema");
+  }
+  const expected: Readonly<Record<string, unknown>> = {
+    schema_version: 1, engine_id: SENTRDEL_ENGINE_ID,
+    engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
+    engine_version: SENTRDEL_ENGINE_VERSION,
+    capability_id: SENTRDEL_CONFIG_PRESENCE_CAPABILITY,
+  };
+  for (const [k, v] of Object.entries(expected)) {
+    if (value[k] !== v) reasons.push(k + " violates pinned source");
+  }
+  for (const k of ["request_id", "attempt_id", "producer_id", "evidence_ref"]) {
+    if (typeof value[k] !== "string" || !ID.test(value[k])) reasons.push(k + " must be bounded");
+  }
+  if (typeof value["source_head"] !== "string" || !SHA1.test(value["source_head"])) reasons.push("invalid source head");
+  if (typeof value["evidence_digest"] !== "string" || !SHA256.test(value["evidence_digest"])) reasons.push("invalid evidence digest");
+  if (typeof value["path"] !== "string" || !PATH.test(value["path"]) ||
+      classifySentrdelConfigPresencePathV1(typeof value["path"] === "string" ? value["path"] : "").length === 0) {
+    reasons.push("unrecognized or noncanonical repository path");
+  }
+  if (!SIGNAL_SET.has(value["signal"] as string) ||
+      typeof value["path"] !== "string" ||
+      !classifySentrdelConfigPresencePathV1(value["path"]).includes(value["signal"] as SentrdelPresenceSignalV1)) {
+    reasons.push("signal does not match donor-recognized path");
+  }
+  if (CAPABILITY?.status !== "CHARACTERIZED") reasons.push("config-inspection not characterized");
+  for (const item of Object.values(value)) {
+    if (typeof item === "string" && (containsSecretMaterialV1(item) || containsExternalAttestationV1(item))) {
+      reasons.push("external content contains sensitive or self-attesting text");
+      break;
+    }
+  }
+  return Object.freeze(reasons);
+}
+
+/**
+ * Direct callers cannot mutate or conceal fields between validation and output.
+ * This blocks accessor reads but does not sandbox already executing JS code.
+ */
+export function validateSentrdelConfigPresenceInputV1(value: unknown): readonly string[] {
+  try {
+    return validatePlainSentrdelConfigPresenceInputV1(snapshotSentrdelObservationDataV1(value));
+  } catch {
+    return Object.freeze(["input must be immutable plain JSON data"]);
+  }
+}
+
+/** Normalize a bounded external presence report, not proof that Sentrdel ran. */
+export function normalizeSentrdelConfigPresenceV1(value: unknown): SentrdelConfigPresenceObservationV1 {
+  const stable = snapshotSentrdelObservationDataV1(value);
+  const reasons = validatePlainSentrdelConfigPresenceInputV1(stable);
+  if (reasons.length > 0) throw new TypeError("invalid configuration presence: " + reasons.join("; "));
+  const input = stable as SentrdelConfigPresenceInputV1;
+  const identity = createHash("sha256").update(JSON.stringify([
+    SENTRDEL_CONFIG_PRESENCE_AUTHORITY, input.request_id, input.attempt_id,
+    input.source_head, input.engine_pin, input.engine_tree, input.signal,
+    input.path, input.producer_id, input.evidence_ref, input.evidence_digest,
+  ])).digest("hex");
+  return Object.freeze({
+    schema_version: 1,
+    phase_authority: SENTRDEL_CONFIG_PRESENCE_AUTHORITY,
+    identity: "config-presence:sentrdel:" + identity,
+    source_head: input.source_head,
+    request_id: input.request_id,
+    attempt_id: input.attempt_id,
+    engine_pin: SENTRDEL_PINNED_REVISION,
+    engine_tree: SENTRDEL_PINNED_TREE,
+    pin_ref: SENTRDEL_PIN_REF,
+    capability_id: SENTRDEL_CONFIG_PRESENCE_CAPABILITY,
+    path: input.path,
+    signal: input.signal,
+    provenance: Object.freeze({
+      producer_id: input.producer_id,
+      evidence_ref: input.evidence_ref,
+      evidence_digest: input.evidence_digest,
+    }),
+    authority: "STATIC_PRESENCE_ONLY" as const,
+    assurance_effect: "NONE" as const,
+    producer_execution_attested: false as const,
+    security_rule_executed: false as const,
+    configuration_contents_scanned: false as const,
+    ci_security_scanned: false as const,
+    hosted_posture_verified: false as const,
+    repository_total: false as const,
+    finding_emitted: false as const,
+    claim_assessment_emitted: false as const,
+  });
+}
diff --git a/tests/assurance-security-t09b.test.ts b/tests/assurance-security-t09b.test.ts
new file mode 100644
index 0000000..3bf2493
--- /dev/null
+++ b/tests/assurance-security-t09b.test.ts
@@ -0,0 +1,144 @@
+import { describe, expect, it } from "vitest";
+import {
+  SENTRDEL_CONFIG_PRESENCE_SIGNALS,
+  classifySentrdelConfigPresencePathV1,
+  normalizeSentrdelConfigPresenceV1,
+  validateSentrdelConfigPresenceInputV1,
+  type SentrdelConfigPresenceInputV1,
+} from "../src/assurance/security/sentrdel-config-presence.js";
+import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
+import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
+
+function input(extra: Record<string, unknown> = {}): SentrdelConfigPresenceInputV1 {
+  return {
+    schema_version: 1, request_id: "request:ci", attempt_id: "attempt:1",
+    source_head: "a".repeat(40), engine_id: SENTRDEL_ENGINE_ID,
+    engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
+    engine_version: SENTRDEL_ENGINE_VERSION, capability_id: "config-inspection",
+    path: ".gitlab-ci.yml", signal: "gitlab-ci",
+    producer_id: "producer:sentrdel", evidence_ref: "evidence:fixture",
+    evidence_digest: "b".repeat(64), ...extra,
+  } as SentrdelConfigPresenceInputV1;
+}
+
+describe("UA-P06-T09B pinned static CI/MCP presence", () => {
+  it("classifies only the pinned donor source's path-only signals", () => {
+    const fixtures = [
+      [".github/workflows/check.yml", "github-actions"],
+      ["root/.gitlab-ci.yaml", "gitlab-ci"],
+      ["build/azure-pipelines.yml", "azure-pipelines"],
+      ["Jenkinsfile", "jenkins"],
+      ["ci/Jenkinsfile", "jenkins"],
+      [".circleci/config.yaml", "circleci"],
+      [".mcp.json", "mcp-json"],
+      ["mcp.json", "mcp-json"],
+      [".cursor/mcp.json", "cursor-mcp"],
+      [".vscode/mcp.json", "vscode-mcp"],
+      [".claude/mcp.json", "claude-mcp"],
+      ["supabase/config.toml", "supabase-config"],
+      ["supabase/seed.sql", "supabase-seed"],
+      ["supabase/migrations/20261008_init.sql", "supabase-migration"],
+      ["supabase/functions/webhook/index.ts", "supabase-function"],
+    ] as const;
+    for (const [path, signal] of fixtures) {
+      expect(classifySentrdelConfigPresencePathV1(path)).toContain(signal);
+      const record = normalizeSentrdelConfigPresenceV1(input({ path, signal }));
+      expect(record.path).toBe(path);
+      expect(record.signal).toBe(signal);
+      expect(record.authority).toBe("STATIC_PRESENCE_ONLY");
+      expect(record.assurance_effect).toBe("NONE");
+      expect(record.producer_execution_attested).toBe(false);
+      expect(record.ci_security_scanned).toBe(false);
+      expect(record.hosted_posture_verified).toBe(false);
+      expect(record.finding_emitted).toBe(false);
+    }
+    expect(SENTRDEL_CONFIG_PRESENCE_SIGNALS).toHaveLength(13);
+  });
+
+  it("rejects false positive paths and traversal", () => {
+    for (const path of [
+      "docs/.github/workflows/check.yml", "ci/gitlab.yaml",
+      ".circleci/fake.txt", "docs/mcp.json", ".cursor/config.json",
+      "ci/test.yml", "../.gitlab-ci.yml",
+      "folder/../Jenkinsfile", "/Jenkinsfile", "C:/Jenkinsfile",
+      ".claude/../mcp.json", "src//Jenkinsfile", "config.txt",
+      ".github/workflows/run.json", ".circleci/config.yaml/extra",
+      "docs/supabase/config.toml", "supabase/migrations/dir/nested.sql",
+      "supabase/functions/worker", "supabase/migrations/init.txt",
+      "supabase/functions.txt", "supabase/seed.csv",
+    ]) {
+      expect(classifySentrdelConfigPresencePathV1(path)).toEqual([]);
+      expect(validateSentrdelConfigPresenceInputV1(input({ path }))).not.toEqual([]);
+    }
+  });
+
+  it("never invents coverage, verified security, or runtime execution", () => {
+    const value = normalizeSentrdelConfigPresenceV1(input());
+    expect(value.phase_authority).toBe("UA-P06-T09");
+    expect(value.repository_total).toBe(false);
+    expect(value.configuration_contents_scanned).toBe(false);
+    expect(value.security_rule_executed).toBe(false);
+    expect(value.claim_assessment_emitted).toBe(false);
+    expect(Object.isFrozen(value)).toBe(true);
+    expect(Object.isFrozen(value.provenance)).toBe(true);
+    expect(JSON.stringify(value)).not.toMatch(/"PASS"|"SUPPORTED"|"VERIFIED"/u);
+  });
+
+  it("binds stable identity to producer, evidence and source", () => {
+    const value = normalizeSentrdelConfigPresenceV1(input());
+    expect(value).toEqual(normalizeSentrdelConfigPresenceV1(input()));
+    for (const modification of [
+      { source_head: "c".repeat(40) }, { producer_id: "producer:other" },
+      { evidence_ref: "evidence:other" }, { evidence_digest: "d".repeat(64) },
+      { path: "ci/Jenkinsfile", signal: "jenkins" },
+    ]) {
+      expect(normalizeSentrdelConfigPresenceV1(input(modification)).identity).not.toBe(value.identity);
+    }
+  });
+
+  it("refuses unqualified engine identities, scope promotions, and secrets", () => {
+    const invalid = [
+      { schema_version: 2 }, { engine_pin: "a".repeat(40) },
+      { engine_tree: "b".repeat(40) }, { engine_id: "engine:fake" },
+      { engine_version: "1.0" }, { capability_id: "iac-generic" },
+      { source_head: "broken" }, { producer_id: "" },
+      { evidence_ref: "" }, { evidence_digest: "bad" },
+      { signal: "circleci" }, { signal: "fake-ci" }, { signal: "github-actions" },
+      { security_verdict: "PASS" }, { severity: "critical" },
+      { execution_state: "EXECUTED" }, { hosted_state: "SECURE" },
+      { producer_id: "ghp_" + "x".repeat(36) },
+      { request_id: "-----BEGIN PRIVATE KEY-----" },
+    ];
+    for (const change of invalid) {
+      const result = validateSentrdelConfigPresenceInputV1(input(change));
+      expect(result.length, JSON.stringify(change)).toBeGreaterThan(0);
+      expect(() => normalizeSentrdelConfigPresenceV1(input(change))).toThrow(TypeError);
+    }
+  });
+
+  it("rejects mutable accessors, hidden verdicts and nested input side effects", () => {
+    let reads = 0;
+    const changing = { ...input() };
+    Object.defineProperty(changing, "path", {
+      enumerable: true, get() {
+        reads += 1;
+        return reads === 1 ? ".mcp.json" : "../invalid.json";
+      },
+    });
+    const hidden = { ...input() };
+    Object.defineProperty(hidden, "security_verdict", { value: "PASS", enumerable: false });
+    const symbol = { ...input(), [Symbol("fake")]: "PASS" };
+    for (const item of [changing, hidden, symbol]) {
+      expect(validateSentrdelConfigPresenceInputV1(item).length).toBeGreaterThan(0);
+      expect(() => normalizeSentrdelConfigPresenceV1(item)).toThrow(TypeError);
+    }
+    expect(reads).toBe(0);
+    expect(normalizeSentrdelConfigPresenceV1(input()).authority).toBe("STATIC_PRESENCE_ONLY");
+  });
+
+  it("rejects null/array/scalar and malformed observations", () => {
+    for (const value of [null, undefined, [], 0, "string"]) {
+      expect(validateSentrdelConfigPresenceInputV1(value).length).toBeGreaterThan(0);
+    }
+  });
+});
```

## Full file at head: src/assurance/security/sentrdel-config-presence.ts
```
    1| /**
    2|  * UA-P06-T09, grain B: evidence-bound static CI/MCP/Supabase presence.
    3|  *
    4|  * Exact source: pinned Sentrdel config_detection.rs. This is inventory data
    5|  * only. No config contents, dynamic workflow, CI execution, credentials,
    6|  * remote MCP service, or hosted security posture are inspected.
    7|  */
    8| import { createHash } from "node:crypto";
    9| import { snapshotSentrdelObservationDataV1 } from "./sentrdel-observation-snapshot.js";
   10| import {
   11|   buildSentrdelCapabilitiesV1,
   12|   getSentrdelCapabilityV1,
   13| } from "./sentrdel-capability-characterization.js";
   14| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "./sentrdel-engine-boundary.js";
   15| import { containsSecretMaterialV1, containsExternalAttestationV1 } from "./sentrdel-evidence-normalization.js";
   16| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE, SENTRDEL_PIN_REF } from "./sentrdel-source-pin.js";
   17| 
   18| export const SENTRDEL_CONFIG_PRESENCE_AUTHORITY = "UA-P06-T09" as const;
   19| export const SENTRDEL_CONFIG_PRESENCE_CAPABILITY = "config-inspection" as const;
   20| export const SENTRDEL_CONFIG_PRESENCE_SIGNALS = [
   21|   "github-actions", "gitlab-ci", "azure-pipelines", "jenkins", "circleci",
   22|   "mcp-json", "cursor-mcp", "vscode-mcp", "claude-mcp",
   23|   "supabase-config", "supabase-seed", "supabase-migration", "supabase-function",
   24| ] as const;
   25| export type SentrdelPresenceSignalV1 = (typeof SENTRDEL_CONFIG_PRESENCE_SIGNALS)[number];
   26| const SIGNAL_SET = new Set<string>(SENTRDEL_CONFIG_PRESENCE_SIGNALS);
   27| const CAPABILITY = getSentrdelCapabilityV1(buildSentrdelCapabilitiesV1(), "config-inspection");
   28| const SHA1 = /^[0-9a-f]{40}$/u;
   29| const SHA256 = /^[0-9a-f]{64}$/u;
   30| const ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
   31| const PATH = /^[A-Za-z0-9._/-]{1,4096}$/u;
   32| const EXACT_KEYS = [
   33|   "schema_version", "request_id", "attempt_id", "source_head", "engine_id",
   34|   "engine_pin", "engine_tree", "engine_version", "capability_id",
   35|   "path", "signal", "producer_id", "evidence_ref", "evidence_digest",
   36| ] as const;
   37| 
   38| export interface SentrdelConfigPresenceInputV1 {
   39|   readonly schema_version: 1;
   40|   readonly request_id: string;
   41|   readonly attempt_id: string;
   42|   readonly source_head: string;
   43|   readonly engine_id: typeof SENTRDEL_ENGINE_ID;
   44|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   45|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   46|   readonly engine_version: typeof SENTRDEL_ENGINE_VERSION;
   47|   readonly capability_id: typeof SENTRDEL_CONFIG_PRESENCE_CAPABILITY;
   48|   readonly path: string;
   49|   readonly signal: SentrdelPresenceSignalV1;
   50|   readonly producer_id: string;
   51|   readonly evidence_ref: string;
   52|   readonly evidence_digest: string;
   53| }
   54| 
   55| export interface SentrdelConfigPresenceObservationV1 {
   56|   readonly schema_version: 1;
   57|   readonly phase_authority: typeof SENTRDEL_CONFIG_PRESENCE_AUTHORITY;
   58|   readonly identity: string;
   59|   readonly source_head: string;
   60|   readonly request_id: string;
   61|   readonly attempt_id: string;
   62|   readonly engine_pin: typeof SENTRDEL_PINNED_REVISION;
   63|   readonly engine_tree: typeof SENTRDEL_PINNED_TREE;
   64|   readonly pin_ref: typeof SENTRDEL_PIN_REF;
   65|   readonly capability_id: typeof SENTRDEL_CONFIG_PRESENCE_CAPABILITY;
   66|   readonly path: string;
   67|   readonly signal: SentrdelPresenceSignalV1;
   68|   readonly provenance: Readonly<{ producer_id: string; evidence_ref: string; evidence_digest: string }>;
   69|   readonly authority: "STATIC_PRESENCE_ONLY";
   70|   readonly assurance_effect: "NONE";
   71|   readonly producer_execution_attested: false;
   72|   readonly security_rule_executed: false;
   73|   readonly configuration_contents_scanned: false;
   74|   readonly ci_security_scanned: false;
   75|   readonly hosted_posture_verified: false;
   76|   readonly repository_total: false;
   77|   readonly finding_emitted: false;
   78|   readonly claim_assessment_emitted: false;
   79| }
   80| 
   81| function isRecord(value: unknown): value is Record<string, unknown> {
   82|   return typeof value === "object" && value !== null && !Array.isArray(value);
   83| }
   84| 
   85| /**
   86|  * Transcribes the pinned path-only producer classification. A recognized CI
   87|  * filename is not evidence that any of its instructions were evaluated.
   88|  */
   89| export function classifySentrdelConfigPresencePathV1(path: string): readonly SentrdelPresenceSignalV1[] {
   90|   if (!PATH.test(path) || path.startsWith("/") || path.endsWith("/") ||
   91|       path.split("/").some(part => part === "" || part === "." || part === "..")) {
   92|     return Object.freeze([]);
   93|   }
   94|   const base = path.slice(path.lastIndexOf("/") + 1);
   95|   const signals: SentrdelPresenceSignalV1[] = [];
   96|   if (path.startsWith(".github/workflows/") && /\.ya?ml$/u.test(path)) signals.push("github-actions");
   97|   if (base === ".gitlab-ci.yml" || base === ".gitlab-ci.yaml") signals.push("gitlab-ci");
   98|   if (base === "azure-pipelines.yml" || base === "azure-pipelines.yaml") signals.push("azure-pipelines");
   99|   if (base === "Jenkinsfile") signals.push("jenkins");
  100|   if (path.startsWith(".circleci/") && ["CircleCI.yml", "CircleCI.yaml", "config.yml", "config.yaml"].includes(base)) signals.push("circleci");
  101|   if (path === ".mcp.json" || path === "mcp.json") signals.push("mcp-json");
  102|   if (path === ".cursor/mcp.json") signals.push("cursor-mcp");
  103|   if (path === ".vscode/mcp.json") signals.push("vscode-mcp");
  104|   if (path.startsWith(".claude/") && base === "mcp.json") signals.push("claude-mcp");
  105|   // Pinned supabase_detection.rs recognizes local path layout, not live posture.
  106|   if (path === "supabase/config.toml") signals.push("supabase-config");
  107|   if (path === "supabase/seed.sql") signals.push("supabase-seed");
  108|   if (path.startsWith("supabase/migrations/")) {
  109|     const relative = path.slice("supabase/migrations/".length);
  110|     if (relative.length > 0 && !relative.includes("/") && relative.endsWith(".sql")) {
  111|       signals.push("supabase-migration");
  112|     }
  113|   }
  114|   if (path.startsWith("supabase/functions/")) {
  115|     const parts = path.slice("supabase/functions/".length).split("/");
  116|     if (parts.length >= 2 && parts[0]!.length > 0 && parts[1]!.length > 0) {
  117|       signals.push("supabase-function");
  118|     }
  119|   }
  120|   return Object.freeze(signals);
  121| }
  122| 
  123| function validatePlainSentrdelConfigPresenceInputV1(value: unknown): readonly string[] {
  124|   const reasons: string[] = [];
  125|   if (!isRecord(value)) return Object.freeze(["input must be a record"]);
  126|   if (Object.keys(value).length !== EXACT_KEYS.length ||
  127|       Object.keys(value).some(key => !(EXACT_KEYS as readonly string[]).includes(key))) {
  128|     reasons.push("input keys must exactly match schema");
  129|   }
  130|   const expected: Readonly<Record<string, unknown>> = {
  131|     schema_version: 1, engine_id: SENTRDEL_ENGINE_ID,
  132|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
  133|     engine_version: SENTRDEL_ENGINE_VERSION,
  134|     capability_id: SENTRDEL_CONFIG_PRESENCE_CAPABILITY,
  135|   };
  136|   for (const [k, v] of Object.entries(expected)) {
  137|     if (value[k] !== v) reasons.push(k + " violates pinned source");
  138|   }
  139|   for (const k of ["request_id", "attempt_id", "producer_id", "evidence_ref"]) {
  140|     if (typeof value[k] !== "string" || !ID.test(value[k])) reasons.push(k + " must be bounded");
  141|   }
  142|   if (typeof value["source_head"] !== "string" || !SHA1.test(value["source_head"])) reasons.push("invalid source head");
  143|   if (typeof value["evidence_digest"] !== "string" || !SHA256.test(value["evidence_digest"])) reasons.push("invalid evidence digest");
  144|   if (typeof value["path"] !== "string" || !PATH.test(value["path"]) ||
  145|       classifySentrdelConfigPresencePathV1(typeof value["path"] === "string" ? value["path"] : "").length === 0) {
  146|     reasons.push("unrecognized or noncanonical repository path");
  147|   }
  148|   if (!SIGNAL_SET.has(value["signal"] as string) ||
  149|       typeof value["path"] !== "string" ||
  150|       !classifySentrdelConfigPresencePathV1(value["path"]).includes(value["signal"] as SentrdelPresenceSignalV1)) {
  151|     reasons.push("signal does not match donor-recognized path");
  152|   }
  153|   if (CAPABILITY?.status !== "CHARACTERIZED") reasons.push("config-inspection not characterized");
  154|   for (const item of Object.values(value)) {
  155|     if (typeof item === "string" && (containsSecretMaterialV1(item) || containsExternalAttestationV1(item))) {
  156|       reasons.push("external content contains sensitive or self-attesting text");
  157|       break;
  158|     }
  159|   }
  160|   return Object.freeze(reasons);
  161| }
  162| 
  163| /**
  164|  * Direct callers cannot mutate or conceal fields between validation and output.
  165|  * This blocks accessor reads but does not sandbox already executing JS code.
  166|  */
  167| export function validateSentrdelConfigPresenceInputV1(value: unknown): readonly string[] {
  168|   try {
  169|     return validatePlainSentrdelConfigPresenceInputV1(snapshotSentrdelObservationDataV1(value));
  170|   } catch {
  171|     return Object.freeze(["input must be immutable plain JSON data"]);
  172|   }
  173| }
  174| 
  175| /** Normalize a bounded external presence report, not proof that Sentrdel ran. */
  176| export function normalizeSentrdelConfigPresenceV1(value: unknown): SentrdelConfigPresenceObservationV1 {
  177|   const stable = snapshotSentrdelObservationDataV1(value);
  178|   const reasons = validatePlainSentrdelConfigPresenceInputV1(stable);
  179|   if (reasons.length > 0) throw new TypeError("invalid configuration presence: " + reasons.join("; "));
  180|   const input = stable as SentrdelConfigPresenceInputV1;
  181|   const identity = createHash("sha256").update(JSON.stringify([
  182|     SENTRDEL_CONFIG_PRESENCE_AUTHORITY, input.request_id, input.attempt_id,
  183|     input.source_head, input.engine_pin, input.engine_tree, input.signal,
  184|     input.path, input.producer_id, input.evidence_ref, input.evidence_digest,
  185|   ])).digest("hex");
  186|   return Object.freeze({
  187|     schema_version: 1,
  188|     phase_authority: SENTRDEL_CONFIG_PRESENCE_AUTHORITY,
  189|     identity: "config-presence:sentrdel:" + identity,
  190|     source_head: input.source_head,
  191|     request_id: input.request_id,
  192|     attempt_id: input.attempt_id,
  193|     engine_pin: SENTRDEL_PINNED_REVISION,
  194|     engine_tree: SENTRDEL_PINNED_TREE,
  195|     pin_ref: SENTRDEL_PIN_REF,
  196|     capability_id: SENTRDEL_CONFIG_PRESENCE_CAPABILITY,
  197|     path: input.path,
  198|     signal: input.signal,
  199|     provenance: Object.freeze({
  200|       producer_id: input.producer_id,
  201|       evidence_ref: input.evidence_ref,
  202|       evidence_digest: input.evidence_digest,
  203|     }),
  204|     authority: "STATIC_PRESENCE_ONLY" as const,
  205|     assurance_effect: "NONE" as const,
  206|     producer_execution_attested: false as const,
  207|     security_rule_executed: false as const,
  208|     configuration_contents_scanned: false as const,
  209|     ci_security_scanned: false as const,
  210|     hosted_posture_verified: false as const,
  211|     repository_total: false as const,
  212|     finding_emitted: false as const,
  213|     claim_assessment_emitted: false as const,
  214|   });
  215| }
```

## Full file at head: tests/assurance-security-t09b.test.ts
```
    1| import { describe, expect, it } from "vitest";
    2| import {
    3|   SENTRDEL_CONFIG_PRESENCE_SIGNALS,
    4|   classifySentrdelConfigPresencePathV1,
    5|   normalizeSentrdelConfigPresenceV1,
    6|   validateSentrdelConfigPresenceInputV1,
    7|   type SentrdelConfigPresenceInputV1,
    8| } from "../src/assurance/security/sentrdel-config-presence.js";
    9| import { SENTRDEL_ENGINE_ID, SENTRDEL_ENGINE_VERSION } from "../src/assurance/security/sentrdel-engine-boundary.js";
   10| import { SENTRDEL_PINNED_REVISION, SENTRDEL_PINNED_TREE } from "../src/assurance/security/sentrdel-source-pin.js";
   11| 
   12| function input(extra: Record<string, unknown> = {}): SentrdelConfigPresenceInputV1 {
   13|   return {
   14|     schema_version: 1, request_id: "request:ci", attempt_id: "attempt:1",
   15|     source_head: "a".repeat(40), engine_id: SENTRDEL_ENGINE_ID,
   16|     engine_pin: SENTRDEL_PINNED_REVISION, engine_tree: SENTRDEL_PINNED_TREE,
   17|     engine_version: SENTRDEL_ENGINE_VERSION, capability_id: "config-inspection",
   18|     path: ".gitlab-ci.yml", signal: "gitlab-ci",
   19|     producer_id: "producer:sentrdel", evidence_ref: "evidence:fixture",
   20|     evidence_digest: "b".repeat(64), ...extra,
   21|   } as SentrdelConfigPresenceInputV1;
   22| }
   23| 
   24| describe("UA-P06-T09B pinned static CI/MCP presence", () => {
   25|   it("classifies only the pinned donor source's path-only signals", () => {
   26|     const fixtures = [
   27|       [".github/workflows/check.yml", "github-actions"],
   28|       ["root/.gitlab-ci.yaml", "gitlab-ci"],
   29|       ["build/azure-pipelines.yml", "azure-pipelines"],
   30|       ["Jenkinsfile", "jenkins"],
   31|       ["ci/Jenkinsfile", "jenkins"],
   32|       [".circleci/config.yaml", "circleci"],
   33|       [".mcp.json", "mcp-json"],
   34|       ["mcp.json", "mcp-json"],
   35|       [".cursor/mcp.json", "cursor-mcp"],
   36|       [".vscode/mcp.json", "vscode-mcp"],
   37|       [".claude/mcp.json", "claude-mcp"],
   38|       ["supabase/config.toml", "supabase-config"],
   39|       ["supabase/seed.sql", "supabase-seed"],
   40|       ["supabase/migrations/20261008_init.sql", "supabase-migration"],
   41|       ["supabase/functions/webhook/index.ts", "supabase-function"],
   42|     ] as const;
   43|     for (const [path, signal] of fixtures) {
   44|       expect(classifySentrdelConfigPresencePathV1(path)).toContain(signal);
   45|       const record = normalizeSentrdelConfigPresenceV1(input({ path, signal }));
   46|       expect(record.path).toBe(path);
   47|       expect(record.signal).toBe(signal);
   48|       expect(record.authority).toBe("STATIC_PRESENCE_ONLY");
   49|       expect(record.assurance_effect).toBe("NONE");
   50|       expect(record.producer_execution_attested).toBe(false);
   51|       expect(record.ci_security_scanned).toBe(false);
   52|       expect(record.hosted_posture_verified).toBe(false);
   53|       expect(record.finding_emitted).toBe(false);
   54|     }
   55|     expect(SENTRDEL_CONFIG_PRESENCE_SIGNALS).toHaveLength(13);
   56|   });
   57| 
   58|   it("rejects false positive paths and traversal", () => {
   59|     for (const path of [
   60|       "docs/.github/workflows/check.yml", "ci/gitlab.yaml",
   61|       ".circleci/fake.txt", "docs/mcp.json", ".cursor/config.json",
   62|       "ci/test.yml", "../.gitlab-ci.yml",
   63|       "folder/../Jenkinsfile", "/Jenkinsfile", "C:/Jenkinsfile",
   64|       ".claude/../mcp.json", "src//Jenkinsfile", "config.txt",
   65|       ".github/workflows/run.json", ".circleci/config.yaml/extra",
   66|       "docs/supabase/config.toml", "supabase/migrations/dir/nested.sql",
   67|       "supabase/functions/worker", "supabase/migrations/init.txt",
   68|       "supabase/functions.txt", "supabase/seed.csv",
   69|     ]) {
   70|       expect(classifySentrdelConfigPresencePathV1(path)).toEqual([]);
   71|       expect(validateSentrdelConfigPresenceInputV1(input({ path }))).not.toEqual([]);
   72|     }
   73|   });
   74| 
   75|   it("never invents coverage, verified security, or runtime execution", () => {
   76|     const value = normalizeSentrdelConfigPresenceV1(input());
   77|     expect(value.phase_authority).toBe("UA-P06-T09");
   78|     expect(value.repository_total).toBe(false);
   79|     expect(value.configuration_contents_scanned).toBe(false);
   80|     expect(value.security_rule_executed).toBe(false);
   81|     expect(value.claim_assessment_emitted).toBe(false);
   82|     expect(Object.isFrozen(value)).toBe(true);
   83|     expect(Object.isFrozen(value.provenance)).toBe(true);
   84|     expect(JSON.stringify(value)).not.toMatch(/"PASS"|"SUPPORTED"|"VERIFIED"/u);
   85|   });
   86| 
   87|   it("binds stable identity to producer, evidence and source", () => {
   88|     const value = normalizeSentrdelConfigPresenceV1(input());
   89|     expect(value).toEqual(normalizeSentrdelConfigPresenceV1(input()));
   90|     for (const modification of [
   91|       { source_head: "c".repeat(40) }, { producer_id: "producer:other" },
   92|       { evidence_ref: "evidence:other" }, { evidence_digest: "d".repeat(64) },
   93|       { path: "ci/Jenkinsfile", signal: "jenkins" },
   94|     ]) {
   95|       expect(normalizeSentrdelConfigPresenceV1(input(modification)).identity).not.toBe(value.identity);
   96|     }
   97|   });
   98| 
   99|   it("refuses unqualified engine identities, scope promotions, and secrets", () => {
  100|     const invalid = [
  101|       { schema_version: 2 }, { engine_pin: "a".repeat(40) },
  102|       { engine_tree: "b".repeat(40) }, { engine_id: "engine:fake" },
  103|       { engine_version: "1.0" }, { capability_id: "iac-generic" },
  104|       { source_head: "broken" }, { producer_id: "" },
  105|       { evidence_ref: "" }, { evidence_digest: "bad" },
  106|       { signal: "circleci" }, { signal: "fake-ci" }, { signal: "github-actions" },
  107|       { security_verdict: "PASS" }, { severity: "critical" },
  108|       { execution_state: "EXECUTED" }, { hosted_state: "SECURE" },
  109|       { producer_id: "ghp_" + "x".repeat(36) },
  110|       { request_id: "-----BEGIN PRIVATE KEY-----" },
  111|     ];
  112|     for (const change of invalid) {
  113|       const result = validateSentrdelConfigPresenceInputV1(input(change));
  114|       expect(result.length, JSON.stringify(change)).toBeGreaterThan(0);
  115|       expect(() => normalizeSentrdelConfigPresenceV1(input(change))).toThrow(TypeError);
  116|     }
  117|   });
  118| 
  119|   it("rejects mutable accessors, hidden verdicts and nested input side effects", () => {
  120|     let reads = 0;
  121|     const changing = { ...input() };
  122|     Object.defineProperty(changing, "path", {
  123|       enumerable: true, get() {
  124|         reads += 1;
  125|         return reads === 1 ? ".mcp.json" : "../invalid.json";
  126|       },
  127|     });
  128|     const hidden = { ...input() };
  129|     Object.defineProperty(hidden, "security_verdict", { value: "PASS", enumerable: false });
  130|     const symbol = { ...input(), [Symbol("fake")]: "PASS" };
  131|     for (const item of [changing, hidden, symbol]) {
  132|       expect(validateSentrdelConfigPresenceInputV1(item).length).toBeGreaterThan(0);
  133|       expect(() => normalizeSentrdelConfigPresenceV1(item)).toThrow(TypeError);
  134|     }
  135|     expect(reads).toBe(0);
  136|     expect(normalizeSentrdelConfigPresenceV1(input()).authority).toBe("STATIC_PRESENCE_ONLY");
  137|   });
  138| 
  139|   it("rejects null/array/scalar and malformed observations", () => {
  140|     for (const value of [null, undefined, [], 0, "string"]) {
  141|       expect(validateSentrdelConfigPresenceInputV1(value).length).toBeGreaterThan(0);
  142|     }
  143|   });
  144| });
```
