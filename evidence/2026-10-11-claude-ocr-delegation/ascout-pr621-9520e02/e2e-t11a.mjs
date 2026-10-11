import { pathToFileURL } from "node:url";
import { join } from "node:path";
import { createHash } from "node:crypto";
const root = process.argv[2];
const { importSentrdelSarifV1 } = await import(pathToFileURL(join(root, "dist/assurance/security/sentrdel-sarif-import.js")).href);
// A realistic multi-run SARIF log, including a "pass" result and a suppressed result.
const sarif = JSON.stringify({ version: "2.1.0", $schema: "https://json.schemastore.org/sarif-2.1.0.json", runs: [
  { tool: { driver: { name: "CodeQL", semanticVersion: "2.19.0", rules: [{ id: "js/xss" }] } }, results: [
    { ruleId: "js/xss", level: "error", message: { text: "Cross-site scripting" },
      locations: [{ physicalLocation: { artifactLocation: { uri: "src/web/render%20page.ts" }, region: { startLine: 40, endLine: 42 } } }] },
    { ruleId: "js/xss", kind: "pass", level: "none", message: { text: "No XSS here" }, suppressions: [{ kind: "external" }] } ] },
  { tool: { driver: { name: "Semgrep", version: "1.90.0" } }, results: [] } ] });
const binding = { schema_version: 1, source_head: "c".repeat(40), request_id: "request:e2e", attempt_id: "attempt:1",
  producer_id: "producer:ci", evidence_ref: "evidence:codeql-sarif",
  evidence_digest: createHash("sha256").update(sarif, "utf8").digest("hex"), sarif_text: sarif };
const r = importSentrdelSarifV1(binding);
for (const o of r.observations) console.log(`${o.tool_name}@${o.tool_version} ${o.rule_id} level=${o.reported_level} class=${o.epistemic_class} truth=${o.canonical_truth} paths=${o.locations.map(l => l.path + ":" + l.start_line).join(",") || "-"}`);
console.log("observations", r.observations.length, "empty_import_is_clean", r.empty_import_is_clean, "sarif_is_canonical_truth", r.sarif_is_canonical_truth, "assurance_effect", r.assurance_effect);
let tamperRefused = false;
try { importSentrdelSarifV1({ ...binding, sarif_text: sarif.replace("error", "note") }); } catch { tamperRefused = true; }
console.log("tampered SARIF refused:", tamperRefused);
