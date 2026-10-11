import { pathToFileURL } from "node:url";
import { join } from "node:path";
const root = process.argv[2];
const load = (p) => import(pathToFileURL(join(root, "dist/assurance/security", p)).href);
const { normalizeSentrdelEvidenceV1 } = await load("sentrdel-evidence-normalization.js");
const { assessSentrdelRemediationV1 } = await load("sentrdel-remediation-retest.js");
const { SENTRDEL_ENGINE_ID } = await load("sentrdel-engine-boundary.js");
const pin = await load("sentrdel-source-pin.js");
const BEFORE = "a".repeat(40), AFTER = "b".repeat(40);
const obs = (head, request, digest, rule = "rule:sqli") => normalizeSentrdelEvidenceV1({ schema_version: 1, request_id: request,
  attempt_id: "attempt:1", claim_class: "STRUCTURAL_OBSERVATION", engine_id: SENTRDEL_ENGINE_ID, engine_pin: pin.SENTRDEL_PINNED_REVISION,
  engine_tree: pin.SENTRDEL_PINNED_TREE, engine_version: "0.0.0", source_head: head, capability_id: "sast-structural",
  execution_state: "EXECUTED", rule_id: rule, location: { path: "src/db/query.ts", start_line: 40, end_line: 44 },
  raw_evidence_ref: "raw:" + request, raw_evidence_digest: digest, coverage_state: "PARTIAL", scanned_scope: ["src"],
  unscanned_scope: ["vendor"], unknown_states: ["PARSER_UNSUPPORTED"], limitations: ["e2e"],
  provenance: { state: "COMPLETE", producer_id: "producer:s", producer_version: "0.0.0", collector_ref: "c:1", rule_set_ref: "r:1" },
  effect_facts: "E0_READ_ONLY_ANALYSIS", network_facts: "NO_NETWORK", egress_facts: "NO_EGRESS", reproduction_ref: null });
const original = obs(BEFORE, "request:scan", "1".repeat(64));
const fix = { schema_version: 1, fix_ref: "pr:101", fix_head: AFTER };
const run = (o = {}) => ({ schema_version: 1, source_head: AFTER, request_id: "request:retest", attempt_id: "attempt:1",
  capability_id: "sast-structural", execution_state: "EXECUTED", coverage_state: "COMPLETE_WITHIN_STATED_SCOPE",
  scanned_scope: ["src"], unknown_states: [], evidence_ref: "evidence:retest", evidence_digest: "9".repeat(64), ...o });
const show = (label, r) => console.log(`${label.padEnd(34)} ${r.state.padEnd(24)} open=${r.lifecycle_open} supports=${r.retest_supports_fix} verified=${r.remediation_verified} reasons=${r.incomplete_reasons.join("|") || "-"}`);
show("1. fix merged, no retest", assessSentrdelRemediationV1(original, fix, null, null));
show("2. retest still finds it", assessSentrdelRemediationV1(original, fix, run(), [obs(AFTER, "request:retest", "2".repeat(64))]));
show("3. retest timed out", assessSentrdelRemediationV1(original, fix, run({ execution_state: "TIMEOUT", coverage_state: "PARTIAL" }), []));
show("4. retest scanned only lib/", assessSentrdelRemediationV1(original, fix, run({ scanned_scope: ["lib"] }), []));
show("5. complete retest, not re-found", assessSentrdelRemediationV1(original, fix, run(), [obs(AFTER, "request:retest", "3".repeat(64), "rule:other")]));
