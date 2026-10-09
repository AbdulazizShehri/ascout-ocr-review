import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";

export const MAX_RECORDS = 64;

/** Load one receipt file from the store root. */
export function loadReceipt(root: string, name: string): string {
  return readFileSync(join(root, name), "utf8");
}

/** Return the first `count` records, bounded by MAX_RECORDS. */
export function takeRecords<T>(records: readonly T[], count: number): T[] {
  return records.slice(0, Math.min(count, MAX_RECORDS));
}
