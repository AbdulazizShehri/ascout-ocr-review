You are performing a code review in Alibaba OpenCodeReview (OCR) delegation mode. OCR has already selected the files and supplied the review rules below; you perform the review.

Repository: the current working directory (a Git repository).
Review range: bae9fefe634115e999ad1f9bc606c007a671bb43..168fb209c1a2fd3afe06618018b6f9df6e34f533
Files selected by OCR: src/receipt-store.ts

Instructions:
2. Review ONLY changed (+) lines, focusing on correctness, security, performance, error handling, concurrency, and maintainability, guided by the OCR rules below.
3. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
4. Do not run commands or read files; everything you need is below. Do not modify anything.
5. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"src/receipt-store.ts","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the file at 168fb209c1a2fd3afe06618018b6f9df6e34f533. If there are no High or Medium issues, reply {"comments":[]}.

OCR review rules for src/receipt-store.ts:
### Rule Group 1: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- src/receipt-store.ts

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



## Diff (git diff for the review range)
```diff
diff --git a/src/receipt-store.ts b/src/receipt-store.ts
index 1262181..aef1829 100644
--- a/src/receipt-store.ts
+++ b/src/receipt-store.ts
@@ -1,14 +1,34 @@
-import { readFileSync } from "node:fs";
-import { join, resolve } from "node:path";
+import { lstatSync, readFileSync, realpathSync } from "node:fs";
+import { execFileSync } from "node:child_process";
+import { relative, resolve, isAbsolute, sep } from "node:path";
 
 export const MAX_RECORDS = 64;
+const SHA = /^[0-9a-f]{40}$/u;
 
-/** Load one receipt file from the store root. */
+/**
+ * Load one receipt file; names must stay inside the store root.
+ * Containment is checked on resolved real paths, so links cannot escape.
+ * Precondition: the store is not modified concurrently by an untrusted party.
+ */
 export function loadReceipt(root: string, name: string): string {
-  return readFileSync(join(root, name), "utf8");
+  const base = realpathSync(root);
+  const target = realpathSync(resolve(base, name));
+  const rel = relative(base, target);
+  if (rel === "" || rel === ".." || rel.startsWith(".." + sep) || isAbsolute(rel)) {
+    throw new Error("receipt path escapes the store root");
+  }
+  if (!lstatSync(target).isFile()) throw new Error("receipt must be a regular file");
+  return readFileSync(target, "utf8");
 }
 
 /** Return the first `count` records, bounded by MAX_RECORDS. */
 export function takeRecords<T>(records: readonly T[], count: number): T[] {
-  return records.slice(0, Math.min(count, MAX_RECORDS));
+  const limit = Math.max(0, Math.min(count, MAX_RECORDS, records.length));
+  return records.slice(0, limit);
+}
+
+/** Report the Git object that a receipt is bound to. */
+export function receiptObjectType(root: string, sha: string): string {
+  if (!SHA.test(sha)) throw new Error("sha must be a full lowercase SHA-1");
+  return execFileSync("git", ["-C", root, "cat-file", "-t", sha], { encoding: "utf8" }).trim();
 }
```

## Full file at the head commit, with line numbers
```
   1| import { lstatSync, readFileSync, realpathSync } from "node:fs";
   2| import { execFileSync } from "node:child_process";
   3| import { relative, resolve, isAbsolute, sep } from "node:path";
   4| 
   5| export const MAX_RECORDS = 64;
   6| const SHA = /^[0-9a-f]{40}$/u;
   7| 
   8| /**
   9|  * Load one receipt file; names must stay inside the store root.
  10|  * Containment is checked on resolved real paths, so links cannot escape.
  11|  * Precondition: the store is not modified concurrently by an untrusted party.
  12|  */
  13| export function loadReceipt(root: string, name: string): string {
  14|   const base = realpathSync(root);
  15|   const target = realpathSync(resolve(base, name));
  16|   const rel = relative(base, target);
  17|   if (rel === "" || rel === ".." || rel.startsWith(".." + sep) || isAbsolute(rel)) {
  18|     throw new Error("receipt path escapes the store root");
  19|   }
  20|   if (!lstatSync(target).isFile()) throw new Error("receipt must be a regular file");
  21|   return readFileSync(target, "utf8");
  22| }
  23| 
  24| /** Return the first `count` records, bounded by MAX_RECORDS. */
  25| export function takeRecords<T>(records: readonly T[], count: number): T[] {
  26|   const limit = Math.max(0, Math.min(count, MAX_RECORDS, records.length));
  27|   return records.slice(0, limit);
  28| }
  29| 
  30| /** Report the Git object that a receipt is bound to. */
  31| export function receiptObjectType(root: string, sha: string): string {
  32|   if (!SHA.test(sha)) throw new Error("sha must be a full lowercase SHA-1");
  33|   return execFileSync("git", ["-C", root, "cat-file", "-t", sha], { encoding: "utf8" }).trim();
  34| }
```
