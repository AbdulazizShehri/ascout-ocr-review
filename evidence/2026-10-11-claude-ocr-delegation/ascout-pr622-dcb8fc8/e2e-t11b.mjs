import { pathToFileURL } from "node:url";
import { join } from "node:path";
const root = process.argv[2];
const load = (p) => import(pathToFileURL(join(root, "dist/assurance/security", p)).href);
const { normalizeSentrdelEvidenceV1 } = await load("sentrdel-evidence-normalization.js");
const { exportSentrdelSarifV1 } = await load("sentrdel-sarif-export.js");
const { importSentrdelSarifV1 } = await load("sentrdel-sarif-import.js");
const { SENTRDEL_ENGINE_ID } = await load("sentrdel-engine-boundary.js");
const pin = await load("sentrdel-source-pin.js");
const base = { schema_version: 1, request_id: "request:e2e", attempt_id: "attempt:1", engine_id: SENTRDEL_ENGINE_ID,
  engine_pin: pin.SENTRDEL_PINNED_REVISION, engine_tree: pin.SENTRDEL_PINNED_TREE, engine_version: "0.0.0",
  source_head: "e".repeat(40), execution_state: "EXECUTED", coverage_state: "PARTIAL", unscanned_scope: ["vendor"],
  limitations: ["e2e"], effect_facts: "E0_READ_ONLY_ANALYSIS", network_facts: "NO_NETWORK", egress_facts: "NO_EGRESS" };
const sast = normalizeSentrdelEvidenceV1({ ...base, claim_class: "STRUCTURAL_OBSERVATION", capability_id: "sast-structural",
  rule_id: "rule:eval-order", location: { path: "src/app.ts", start_line: 12, end_line: 18 }, raw_evidence_ref: "raw:1",
  raw_evidence_digest: "1".repeat(64), scanned_scope: ["src/app.ts"], unknown_states: ["PARSER_UNSUPPORTED"],
  provenance: { state: "COMPLETE", producer_id: "producer:s", producer_version: "0.0.0", collector_ref: "c:1", rule_set_ref: "r:1" },
  reproduction_ref: "repro:1" });
const dep = normalizeSentrdelEvidenceV1({ ...base, claim_class: "DEPENDENCY_OBSERVATION", capability_id: "dependency-delta",
  rule_id: null, location: { path: "package-lock.json", start_line: null, end_line: null }, raw_evidence_ref: "raw:2",
  raw_evidence_digest: "2".repeat(64), scanned_scope: ["package-lock.json"], unknown_states: ["REACHABILITY_NOT_COMPUTED"],
  provenance: { state: "ABSENT", producer_id: null, producer_version: null, collector_ref: null, rule_set_ref: null },
  reproduction_ref: null });
const out = exportSentrdelSarifV1([dep, sast]);
const log = JSON.parse(out.sarif_text);
for (const r of log.runs[0].results) console.log(`${r.ruleId} kind=${r.kind} level=${r.level} uri=${r.locations[0]?.physicalLocation.artifactLocation.uri ?? "-"} region=${JSON.stringify(r.locations[0]?.physicalLocation.region ?? null)} truth=${r.properties.ascout_canonical_truth}`);
console.log("run properties", JSON.stringify(log.runs[0].properties));
const back = importSentrdelSarifV1({ schema_version: 1, source_head: "e".repeat(40), request_id: "request:e2e", attempt_id: "attempt:1",
  producer_id: "producer:ascout", evidence_ref: "evidence:export", evidence_digest: out.sarif_digest, sarif_text: out.sarif_text });
console.log("re-imported", back.observations.length, "classes", [...new Set(back.observations.map(o => o.epistemic_class))].join(","), "truth", back.sarif_is_canonical_truth);
let refused = false;
try { exportSentrdelSarifV1([{ ...sast, finding_emitted: true }]); } catch { refused = true; }
console.log("promoted record refused:", refused);
