import { pathToFileURL } from "node:url";
import { join } from "node:path";
const root = process.argv[2];
const load = (p) => import(pathToFileURL(join(root, "dist/assurance/security", p)).href);
const { normalizeSentrdelEvidenceV1 } = await load("sentrdel-evidence-normalization.js");
const { linkSentrdelReproductionV1 } = await load("sentrdel-reproduction-link.js");
const { SENTRDEL_ENGINE_ID } = await load("sentrdel-engine-boundary.js");
const pin = await load("sentrdel-source-pin.js");
const obs = (ref) => normalizeSentrdelEvidenceV1({ schema_version: 1, request_id: "request:e2e", attempt_id: "attempt:1",
  claim_class: "STRUCTURAL_OBSERVATION", engine_id: SENTRDEL_ENGINE_ID, engine_pin: pin.SENTRDEL_PINNED_REVISION,
  engine_tree: pin.SENTRDEL_PINNED_TREE, engine_version: "0.0.0", source_head: "e".repeat(40), capability_id: "sast-structural",
  execution_state: "EXECUTED", rule_id: "rule:eval-order", location: { path: "src/app.ts", start_line: 3, end_line: 9 },
  raw_evidence_ref: "raw:e2e", raw_evidence_digest: "c".repeat(64), coverage_state: "PARTIAL", scanned_scope: ["src/app.ts"],
  unscanned_scope: ["vendor"], unknown_states: ["PARSER_UNSUPPORTED"], limitations: ["e2e"],
  provenance: { state: "COMPLETE", producer_id: "producer:s", producer_version: "0.0.0", collector_ref: "c:1", rule_set_ref: "r:1" },
  effect_facts: "E0_READ_ONLY_ANALYSIS", network_facts: "NO_NETWORK", egress_facts: "NO_EGRESS", reproduction_ref: ref });
const repro = { schema_version: 1, reproduction_ref: "repro:e2e", source_head: "e".repeat(40), method: "deterministic-rescan", input_digest: "c".repeat(64) };
const show = (l) => console.log(`${l.state} ref=${l.reproduction_ref} method=${l.method} executed=${l.reproduction_executed} reproduced=${l.reproduced} exploit_proven=${l.exploit_proven}`);
show(linkSentrdelReproductionV1(obs("repro:e2e"), repro));
show(linkSentrdelReproductionV1(obs("repro:e2e"), null));
show(linkSentrdelReproductionV1(obs(null), null));
for (const [name, bad] of [["foreign digest", { ...repro, input_digest: "d".repeat(64) }], ["other head", { ...repro, source_head: "f".repeat(40) }]]) {
  try { linkSentrdelReproductionV1(obs("repro:e2e"), bad); console.log(name, "ACCEPTED (unexpected)"); } catch { console.log(name, "refused"); }
}
