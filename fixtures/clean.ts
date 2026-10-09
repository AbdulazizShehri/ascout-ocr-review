import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { relative, resolve, isAbsolute, sep } from "node:path";

export const MAX_RECORDS = 64;
const SHA = /^[0-9a-f]{40}$/u;

/** Load one receipt file; names must stay inside the store root. */
export function loadReceipt(root: string, name: string): string {
  const base = resolve(root);
  const target = resolve(base, name);
  const rel = relative(base, target);
  if (rel === "" || rel === ".." || rel.startsWith(".." + sep) || isAbsolute(rel)) {
    throw new Error("receipt path escapes the store root");
  }
  return readFileSync(target, "utf8");
}

/** Return the first `count` records, bounded by MAX_RECORDS. */
export function takeRecords<T>(records: readonly T[], count: number): T[] {
  const limit = Math.max(0, Math.min(count, MAX_RECORDS, records.length));
  return records.slice(0, limit);
}

/** Report the Git object that a receipt is bound to. */
export function receiptObjectType(root: string, sha: string): string {
  if (!SHA.test(sha)) throw new Error("sha must be a full lowercase SHA-1");
  return execFileSync("git", ["-C", root, "cat-file", "-t", sha], { encoding: "utf8" }).trim();
}
