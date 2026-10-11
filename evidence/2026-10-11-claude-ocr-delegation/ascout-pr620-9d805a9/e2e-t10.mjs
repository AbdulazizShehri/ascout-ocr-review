import { pathToFileURL } from "node:url";
import { join } from "node:path";
const root = process.argv[2];
const load = (p) => import(pathToFileURL(join(root, "dist/assurance/security", p)).href);
const m = await load("sentrdel-invariant-regression.js");
const pin = await load("sentrdel-source-pin.js");
const eng = await load("sentrdel-engine-boundary.js");
const side = (role, head, evaluations) => ({ schema_version: 1, role, source_head: head.repeat(40),
  request_id: "request:e2e", attempt_id: "attempt:1", engine_id: eng.SENTRDEL_ENGINE_ID,
  engine_pin: pin.SENTRDEL_PINNED_REVISION, engine_tree: pin.SENTRDEL_PINNED_TREE,
  engine_version: eng.SENTRDEL_ENGINE_VERSION, producer_id: "producer:e2e",
  evidence_ref: "evidence:" + role.toLowerCase(), evidence_digest: (head === "a" ? "1" : "2").repeat(64), evaluations });
const ev = (id, state, cov = "COVERED") => ({ invariant_id: id, definition_digest: "d".repeat(64), state,
  coverage_state: cov, unknown_tokens: cov === "COVERED" ? [] : ["TIMEOUT"] });
const r = m.compareSentrdelInvariantRegressionV1(
  side("TRUSTED_BASE", "a", [ev("authz:owner-only", "SATISFIED"), ev("csrf:token", "SATISFIED"), ev("secrets:none", "VIOLATED"), ev("legacy:rule", "SATISFIED")]),
  side("CANDIDATE", "b", [ev("authz:owner-only", "VIOLATED"), ev("csrf:token", "SATISFIED", "TIMED_OUT"), ev("secrets:none", "SATISFIED")]));
for (const x of r.records) console.log(`${x.invariant_id} ${x.base_state}>${x.candidate_state}/${x.candidate_coverage} => ${x.disposition} (${x.reason_code})`);
console.log("counts", JSON.stringify(r.disposition_counts), "uncertain", r.uncertain_records,
  "candidate_clean_claimed", r.candidate_clean_claimed, "remediation_verified", r.remediation_verified, "assurance_effect", r.assurance_effect);
let refused = false;
try { m.compareSentrdelInvariantRegressionV1(side("TRUSTED_BASE", "a", [ev("x", "SATISFIED")]), side("CANDIDATE", "a", [ev("x", "SATISFIED")])); } catch { refused = true; }
console.log("same-revision comparison refused:", refused);
