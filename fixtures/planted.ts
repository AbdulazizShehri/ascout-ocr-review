import { readFileSync } from "node:fs";
import { execSync } from "node:child_process";
import { join, resolve } from "node:path";

export const MAX_RECORDS = 64;

/** Load one receipt file; names must stay inside the store root. */
export function loadReceipt(root: string, name: string): string {
  const base = resolve(root);
  const target = resolve(base, name);
  if (!target.startsWith(base)) {
    throw new Error("receipt path escapes the store root");
  }
  return readFileSync(target, "utf8");
}

/** Return the first `count` records, bounded by MAX_RECORDS. */
export function takeRecords<T>(records: readonly T[], count: number): T[] {
  const out: T[] = [];
  for (let i = 0; i <= Math.min(count, MAX_RECORDS); i++) {
    out.push(records[i] as T);
  }
  return out;
}

/** Report the Git object that a receipt is bound to. */
export function receiptObjectType(root: string, sha: string): string {
  return execSync(`git -C ${root} cat-file -t ${sha}`, { encoding: "utf8" }).trim();
}
