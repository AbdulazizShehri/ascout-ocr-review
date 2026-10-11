You are performing a code review in Alibaba OpenCodeReview (OCR) delegation mode. OCR has already selected the files and supplied the review rules below; you perform the review.

Repository: the current working directory (a Git repository).
Review range: bae9fefe634115e999ad1f9bc606c007a671bb43..4b763981886e7e79893bca52a018f7a7e0c028c1
Files selected by OCR: src/receipt-store.ts

Instructions:
2. Review ONLY changed (+) lines, focusing on correctness, security, performance, error handling, concurrency, and maintainability, guided by the OCR rules below.
3. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
4. Do not run commands or read files; everything you need is below. Do not modify anything.
5. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"src/receipt-store.ts","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the file at 4b763981886e7e79893bca52a018f7a7e0c028c1. If there are no High or Medium issues, reply {"comments":[]}.

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
index 1262181..6c33d61 100644
--- a/src/receipt-store.ts
+++ b/src/receipt-store.ts
@@ -1,14 +1,29 @@
 import { readFileSync } from "node:fs";
+import { execSync } from "node:child_process";
 import { join, resolve } from "node:path";
 
 export const MAX_RECORDS = 64;
 
-/** Load one receipt file from the store root. */
+/** Load one receipt file; names must stay inside the store root. */
 export function loadReceipt(root: string, name: string): string {
-  return readFileSync(join(root, name), "utf8");
+  const base = resolve(root);
+  const target = resolve(base, name);
+  if (!target.startsWith(base)) {
+    throw new Error("receipt path escapes the store root");
+  }
+  return readFileSync(target, "utf8");
 }
 
 /** Return the first `count` records, bounded by MAX_RECORDS. */
 export function takeRecords<T>(records: readonly T[], count: number): T[] {
-  return records.slice(0, Math.min(count, MAX_RECORDS));
+  const out: T[] = [];
+  for (let i = 0; i <= Math.min(count, MAX_RECORDS); i++) {
+    out.push(records[i] as T);
+  }
+  return out;
+}
+
+/** Report the Git object that a receipt is bound to. */
+export function receiptObjectType(root: string, sha: string): string {
+  return execSync(`git -C ${root} cat-file -t ${sha}`, { encoding: "utf8" }).trim();
 }
```

## Full file at the head commit, with line numbers
```
   1| import { readFileSync } from "node:fs";
   2| import { execSync } from "node:child_process";
   3| import { join, resolve } from "node:path";
   4| 
   5| export const MAX_RECORDS = 64;
   6| 
   7| /** Load one receipt file; names must stay inside the store root. */
   8| export function loadReceipt(root: string, name: string): string {
   9|   const base = resolve(root);
  10|   const target = resolve(base, name);
  11|   if (!target.startsWith(base)) {
  12|     throw new Error("receipt path escapes the store root");
  13|   }
  14|   return readFileSync(target, "utf8");
  15| }
  16| 
  17| /** Return the first `count` records, bounded by MAX_RECORDS. */
  18| export function takeRecords<T>(records: readonly T[], count: number): T[] {
  19|   const out: T[] = [];
  20|   for (let i = 0; i <= Math.min(count, MAX_RECORDS); i++) {
  21|     out.push(records[i] as T);
  22|   }
  23|   return out;
  24| }
  25| 
  26| /** Report the Git object that a receipt is bound to. */
  27| export function receiptObjectType(root: string, sha: string): string {
  28|   return execSync(`git -C ${root} cat-file -t ${sha}`, { encoding: "utf8" }).trim();
  29| }
```
