You are performing an independent code review of a pull request in Alibaba OpenCodeReview (OCR) delegation mode. OCR supplied the file selection and review rules below; you perform the review. You did not write this code.

Repository: Ascout (TypeScript CLI for verification receipts). Review range: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad..baeff552a47eab43e80580b558928179027793e2
Pull request title (context only): security(deps): patch Vitest path traversal and brace-expansion DoS
Changed files: THIRD_PARTY_NOTICES.md,package-lock.json,package.json,tests/vitest-check.integration.test.ts

Instructions:
1. Review ONLY the changed lines in the diff below, using the full files for context. Focus on correctness, security, performance, error handling, concurrency, maintainability, and whether tests keep their assertion strength.
2. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
3. Do not run commands or read files; everything you need is below. Do not modify anything.
4. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"<file>","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|test|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the files at the head commit. If there are no High or Medium issues, reply {"comments":[]}.

## OCR file selection
# Files (1 reviewable / 4 total)

- mode: range
- from: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- to: baeff552a47eab43e80580b558928179027793e2
- merge_base: ca6b6f514e5a8881e2cfa2789b5e5ea43e3aaaad
- total_insertions: 70
- total_deletions: 70

~~- `THIRD_PARTY_NOTICES.md` [modified] +8/-8 (excluded: unsupported_ext)~~
~~- `package-lock.json` [modified] +58/-58 (excluded: default_path)~~
  - `package.json` [modified] +2/-2
~~- `tests/vitest-check.integration.test.ts` [modified] +2/-2 (excluded: default_path)~~

## OCR review rules
### Rule Group 1: system / **/*.{json,json5}

Applies to:
- package-lock.json

#### Content

Check JSON files for spelling errors in json-keys; ignore the content of json-values.

---

### Rule Group 2: system / **/package.json

Applies to:
- package.json

#### Content

- Avoid introducing dependencies with a version of `latest` or `*`; use specific version numbers instead. Note: ignore this rule when the version number is not on a newly added line of code
- Dependency conflicts or duplicate declarations: the same dependency exists in both `dependencies` and `devDependencies`
- Required tool dependencies not declared: tool names such as eslint, jest, or prettier appear in `scripts` but are not listed in `devDependencies`

---

### Rule Group 3: system / **/*.{ts,js,tsx,jsx,mjs,cjs}

Applies to:
- tests/vitest-check.integration.test.ts

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

## Diff
```diff
diff --git a/THIRD_PARTY_NOTICES.md b/THIRD_PARTY_NOTICES.md
index 449b24a..f2d315b 100644
--- a/THIRD_PARTY_NOTICES.md
+++ b/THIRD_PARTY_NOTICES.md
@@ -72,13 +72,13 @@ This conclusion is scoped to the exact direct package versions below. Transitive
 - Registry tarball: `https://registry.npmjs.org/@types/node/-/node-22.20.1.tgz`
 - SRI: `sha512-EANqOCF9QFyra+4pfxUcX9STKJpCLjMbObVzljIJomAWSnuSIEAvyzEU53GaajbXJEgdh0iEcPL+DGvpUd4k1Q==`
 
-### `@vitest/coverage-v8` 4.1.10
+### `@vitest/coverage-v8` 4.1.11
 
 - Role: development-only V8 coverage provider used by the Vitest integration and changed-code exercise tests
 - License: MIT
-- Upstream: `vitest-dev/vitest`, tag `v4.1.10`, package path `packages/coverage-v8`
-- Registry tarball: `https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.10.tgz`
-- SRI: `sha512-IM49HmthevbgAO4anp1hwtoT9wYe59w0LR00gr+eagHE+ZJ5lK4sLPeO0ubgoJcwLk6dehU3R24N+FbEEKDc8g==`
+- Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/coverage-v8`
+- Registry tarball: `https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.11.tgz`
+- SRI: `sha512-8MVGEFnJIcdGjcbfKmeq8z0pZHH0JlVtoVZH9Q/qwUp6wyFnEJUBMrw9DCaj+ra3vShGmhavjalMIhPNxZAUcw==`
 
 ### `jest` 30.4.2
 
@@ -104,13 +104,13 @@ This conclusion is scoped to the exact direct package versions below. Transitive
 - Registry tarball: `https://registry.npmjs.org/vite/-/vite-6.4.3.tgz`
 - SRI: `sha512-NTKlcQjlAK7MlQoyb6LgaqHc8sso/pVyUJYWMws3jg21uTJw/LddqIFPcPqP6PzpgbIcZyKI85sFE4HBrQDA8A==`
 
-### `vitest` 4.1.10
+### `vitest` 4.1.11
 
 - Role: development-only test runner
 - License: MIT
-- Upstream: `vitest-dev/vitest`, tag `v4.1.10`, package path `packages/vitest`
-- Registry tarball: `https://registry.npmjs.org/vitest/-/vitest-4.1.10.tgz`
-- SRI: `sha512-R9jUTe5S4Qb0HCd4TNqpC7oGcrMssMRGXLW80ubjWsW9VH5GF8y1Y0SFLY9AbqSk6nt0PnOx4H4WNJYZ13GUPw==`
+- Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/vitest`
+- Registry tarball: `https://registry.npmjs.org/vitest/-/vitest-4.1.11.tgz`
+- SRI: `sha512-fhACrNXUidIbGSBr5FlbuBkO7VWC1ZyLl0DO4CU2DrQoAPxX84Ysxs+HeGQpii5lZWV1Q4gBZTTu49mF+A6Edw==`
 
 ## Transitive dependencies
 
diff --git a/package-lock.json b/package-lock.json
index 3214fa4..da3d9ed 100644
--- a/package-lock.json
+++ b/package-lock.json
@@ -17,11 +17,11 @@
       },
       "devDependencies": {
         "@types/node": "22.20.1",
-        "@vitest/coverage-v8": "4.1.10",
+        "@vitest/coverage-v8": "4.1.11",
         "jest": "30.4.2",
         "typescript": "6.0.3",
         "vite": "6.4.3",
-        "vitest": "4.1.10"
+        "vitest": "4.1.11"
       },
       "engines": {
         "node": ">=22"
@@ -2382,14 +2382,14 @@
       ]
     },
     "node_modules/@vitest/coverage-v8": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.10.tgz",
-      "integrity": "sha512-IM49HmthevbgAO4anp1hwtoT9wYe59w0LR00gr+eagHE+ZJ5lK4sLPeO0ubgoJcwLk6dehU3R24N+FbEEKDc8g==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.11.tgz",
+      "integrity": "sha512-8MVGEFnJIcdGjcbfKmeq8z0pZHH0JlVtoVZH9Q/qwUp6wyFnEJUBMrw9DCaj+ra3vShGmhavjalMIhPNxZAUcw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
         "@bcoe/v8-coverage": "^1.0.2",
-        "@vitest/utils": "4.1.10",
+        "@vitest/utils": "4.1.11",
         "ast-v8-to-istanbul": "^1.0.0",
         "istanbul-lib-coverage": "^3.2.2",
         "istanbul-lib-report": "^3.0.1",
@@ -2403,8 +2403,8 @@
         "url": "https://opencollective.com/vitest"
       },
       "peerDependencies": {
-        "@vitest/browser": "4.1.10",
-        "vitest": "4.1.10"
+        "@vitest/browser": "4.1.11",
+        "vitest": "4.1.11"
       },
       "peerDependenciesMeta": {
         "@vitest/browser": {
@@ -2413,16 +2413,16 @@
       }
     },
     "node_modules/@vitest/expect": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/expect/-/expect-4.1.10.tgz",
-      "integrity": "sha512-YsCn+qAk1GWjQOWFEsEcL2gNQ0zmVmQu3T03qP6UyjhtmdtwtbuI+DASn/7iQB3HGTXkdBwGddzxPlmiql5vlA==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/expect/-/expect-4.1.11.tgz",
+      "integrity": "sha512-VX2x5vNJXET47KAFzwERI+KRMtTTCSWTfSMKsW7JsUsXV4psq++e3DvZpuTDOpHcxytiDs6p2nhVb2tVDiiUYw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
         "@standard-schema/spec": "^1.1.0",
         "@types/chai": "^5.2.2",
-        "@vitest/spy": "4.1.10",
-        "@vitest/utils": "4.1.10",
+        "@vitest/spy": "4.1.11",
+        "@vitest/utils": "4.1.11",
         "chai": "^6.2.2",
         "tinyrainbow": "^3.1.0"
       },
@@ -2431,13 +2431,13 @@
       }
     },
     "node_modules/@vitest/mocker": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/mocker/-/mocker-4.1.10.tgz",
-      "integrity": "sha512-v0xaezt+DKEmKfaxg133ldzADrwLGd7Ze1MfQQTYfvs8OqZIwbxyxaYURivwV7sWy5fqn3rH5uOrSp07bp44Ow==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/mocker/-/mocker-4.1.11.tgz",
+      "integrity": "sha512-2XJVD55d1o5AZous5CCGKS74g/riOj9odEt2bQpCVZeblHyHdnMeFl4jl0XjU21stf4mbjUkew2eXQZt65g5CQ==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
-        "@vitest/spy": "4.1.10",
+        "@vitest/spy": "4.1.11",
         "estree-walker": "^3.0.3",
         "magic-string": "^0.30.21"
       },
@@ -2458,9 +2458,9 @@
       }
     },
     "node_modules/@vitest/pretty-format": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/pretty-format/-/pretty-format-4.1.10.tgz",
-      "integrity": "sha512-W1HsjSH4MXQ9YfmmhLAoIYf1HRfekQCGngeIgcei6MP5QQGWUe0gkopdZQaVCFO+JDJMrAJGwa5pRpNpvy4P8Q==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/pretty-format/-/pretty-format-4.1.11.tgz",
+      "integrity": "sha512-yiZzPbGTS9Sr/JpFl8zHrcIkAofNbFV6k21vIgQN/cY/oxZeXhJv5sc/MBJ5jFKWmWs+oJHw0UXLZjmf931+Vw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
@@ -2471,13 +2471,13 @@
       }
     },
     "node_modules/@vitest/runner": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/runner/-/runner-4.1.10.tgz",
-      "integrity": "sha512-IKI6kpIH+LmpROplyLwBBaCfMgOZOMsygVa6BARD6ahA04VRuJSa6OaVG7kRvSEMD870Vd91rSSw0eegtWyLGg==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/runner/-/runner-4.1.11.tgz",
+      "integrity": "sha512-LztvUgdwMNJMIkj3hQnnxiC2Xy1zNxq928W/xhjCLaNCzqTZOudjwbQf6v9IntZGPw132i2Lq2rgTRZHD3JHNw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
-        "@vitest/utils": "4.1.10",
+        "@vitest/utils": "4.1.11",
         "pathe": "^2.0.3"
       },
       "funding": {
@@ -2485,14 +2485,14 @@
       }
     },
     "node_modules/@vitest/snapshot": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/snapshot/-/snapshot-4.1.10.tgz",
-      "integrity": "sha512-xRkfOT1qpTAi/Ti4Y1LtfRc3kEuqxGw59eN2jN9pRWMtS/XDevekhcFSqvQqjUNGksfjMJu3Y+oJ+4Ypn2OaJw==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/snapshot/-/snapshot-4.1.11.tgz",
+      "integrity": "sha512-pN7ikn1ON7h8ee4gIAp4AzyK+zBtJPzVbqOgu5LCEh4VaJVbPQcgYQYJIMGQPXVeJJq1fnfazis7a5pFNPahog==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
-        "@vitest/pretty-format": "4.1.10",
-        "@vitest/utils": "4.1.10",
+        "@vitest/pretty-format": "4.1.11",
+        "@vitest/utils": "4.1.11",
         "magic-string": "^0.30.21",
         "pathe": "^2.0.3"
       },
@@ -2501,9 +2501,9 @@
       }
     },
     "node_modules/@vitest/spy": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/spy/-/spy-4.1.10.tgz",
-      "integrity": "sha512-PLf/Ugvoq5wO/b4rwYCR1h2PSIdXz7wnkQFMiUpLdtM7l6pqVFcQIBEHyT1+l+cj7mNwAfZHzqXqDyjvOuwbDw==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/spy/-/spy-4.1.11.tgz",
+      "integrity": "sha512-apNa/prQy2qCeywhnixOHPRCgGNhvg7T4Dapfl1GahLp/R+uhBm5cPyFoNVyqsNd2h1nJxL6BqqdIjiABL60YA==",
       "dev": true,
       "license": "MIT",
       "funding": {
@@ -2511,13 +2511,13 @@
       }
     },
     "node_modules/@vitest/utils": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/@vitest/utils/-/utils-4.1.10.tgz",
-      "integrity": "sha512-fy9am/HWxbaGt/Sawrp90vt6Y6jQwf1RX77cz3uwoJwJVMli/e1IEwRPnMNJ7vKfPTwo0diXifkpPvwH9v7nGA==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/@vitest/utils/-/utils-4.1.11.tgz",
+      "integrity": "sha512-zTCVGpyFsGWBhllOyKlTw/vnr6D9qxsfSDyfbyZmTyjHw5N/VuvzHpHoQjm2ZJzn4RJgx5w4r7V0er69CmLgPQ==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
-        "@vitest/pretty-format": "4.1.10",
+        "@vitest/pretty-format": "4.1.11",
         "convert-source-map": "^2.0.0",
         "tinyrainbow": "^3.1.0"
       },
@@ -2749,9 +2749,9 @@
       }
     },
     "node_modules/brace-expansion": {
-      "version": "2.1.4",
-      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.1.4.tgz",
-      "integrity": "sha512-hGfVzPxthbf3+2yjg/RBs60cB0FhqBS/zvdV/4wn4/BmN0bNMMHPc4V/BbFieqf1TKAGGAHnY4eSjajCl0f2Xg==",
+      "version": "2.1.7",
+      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.1.7.tgz",
+      "integrity": "sha512-uZbew1NqdmPDTMJ8ah1y+b+9QEJrfkXFk3RcTQw3X0jW/xRUvFKsg1CfQdSYGdTbXZWExtU3J3ccxtnfw1Fi0g==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
@@ -5305,9 +5305,9 @@
       }
     },
     "node_modules/test-exclude/node_modules/brace-expansion": {
-      "version": "1.1.18",
-      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.18.tgz",
-      "integrity": "sha512-Edep/X9fGqVNmzKBVsDYIOtD+z1tuezV70LBjdCst9Tqu76lsnvRiZ6oTic1n+/BIwX6QDGAO94PN4N2SADvtw==",
+      "version": "1.1.21",
+      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.21.tgz",
+      "integrity": "sha512-9zeA+KLZNNzglF2TPKRQEDyx6Yby7daAkuy8MiPzpXPsYDWi/DRM8jmwUDxokQjYqBpv5DgPiwD4h4ZZSy1Ujw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
@@ -5613,19 +5613,19 @@
       }
     },
     "node_modules/vitest": {
-      "version": "4.1.10",
-      "resolved": "https://registry.npmjs.org/vitest/-/vitest-4.1.10.tgz",
-      "integrity": "sha512-R9jUTe5S4Qb0HCd4TNqpC7oGcrMssMRGXLW80ubjWsW9VH5GF8y1Y0SFLY9AbqSk6nt0PnOx4H4WNJYZ13GUPw==",
+      "version": "4.1.11",
+      "resolved": "https://registry.npmjs.org/vitest/-/vitest-4.1.11.tgz",
+      "integrity": "sha512-fhACrNXUidIbGSBr5FlbuBkO7VWC1ZyLl0DO4CU2DrQoAPxX84Ysxs+HeGQpii5lZWV1Q4gBZTTu49mF+A6Edw==",
       "dev": true,
       "license": "MIT",
       "dependencies": {
-        "@vitest/expect": "4.1.10",
-        "@vitest/mocker": "4.1.10",
-        "@vitest/pretty-format": "4.1.10",
-        "@vitest/runner": "4.1.10",
-        "@vitest/snapshot": "4.1.10",
-        "@vitest/spy": "4.1.10",
-        "@vitest/utils": "4.1.10",
+        "@vitest/expect": "4.1.11",
+        "@vitest/mocker": "4.1.11",
+        "@vitest/pretty-format": "4.1.11",
+        "@vitest/runner": "4.1.11",
+        "@vitest/snapshot": "4.1.11",
+        "@vitest/spy": "4.1.11",
+        "@vitest/utils": "4.1.11",
         "es-module-lexer": "^2.0.0",
         "expect-type": "^1.3.0",
         "magic-string": "^0.30.21",
@@ -5653,12 +5653,12 @@
         "@edge-runtime/vm": "*",
         "@opentelemetry/api": "^1.9.0",
         "@types/node": "^20.0.0 || ^22.0.0 || >=24.0.0",
-        "@vitest/browser-playwright": "4.1.10",
-        "@vitest/browser-preview": "4.1.10",
-        "@vitest/browser-webdriverio": "4.1.10",
-        "@vitest/coverage-istanbul": "4.1.10",
-        "@vitest/coverage-v8": "4.1.10",
-        "@vitest/ui": "4.1.10",
+        "@vitest/browser-playwright": "4.1.11",
+        "@vitest/browser-preview": "4.1.11",
+        "@vitest/browser-webdriverio": "4.1.11",
+        "@vitest/coverage-istanbul": "4.1.11",
+        "@vitest/coverage-v8": "4.1.11",
+        "@vitest/ui": "4.1.11",
         "happy-dom": "*",
         "jsdom": "*",
         "vite": "^6.0.0 || ^7.0.0 || ^8.0.0"
diff --git a/package.json b/package.json
index e0fabb1..ea1c615 100644
--- a/package.json
+++ b/package.json
@@ -25,10 +25,10 @@
   },
   "devDependencies": {
     "@types/node": "22.20.1",
-    "@vitest/coverage-v8": "4.1.10",
+    "@vitest/coverage-v8": "4.1.11",
     "jest": "30.4.2",
     "typescript": "6.0.3",
     "vite": "6.4.3",
-    "vitest": "4.1.10"
+    "vitest": "4.1.11"
   }
 }
diff --git a/tests/vitest-check.integration.test.ts b/tests/vitest-check.integration.test.ts
index e3aa57d..daa94e1 100644
--- a/tests/vitest-check.integration.test.ts
+++ b/tests/vitest-check.integration.test.ts
@@ -33,7 +33,7 @@ function initializeFixture(): string {
       name: "t051-vitest-check-fixture",
       private: true,
       type: "module",
-      devDependencies: { vitest: "4.1.10", "@vitest/coverage-v8": "4.1.10" },
+      devDependencies: { vitest: "4.1.11", "@vitest/coverage-v8": "4.1.11" },
     }),
   );
   writeFileSync(join(root, "vitest.config.mjs"), "export default { test: { globals: true } };\n");
@@ -155,7 +155,7 @@ describe("T051 runCheck Vitest integration", () => {
       expect(task).toMatchObject({
         status: "PASS",
         tool_name: "vitest",
-        tool_version: "4.1.10",
+        tool_version: "4.1.11",
         execution_admission: "normal",
       });
       expect(task?.argv).toContain("related");
```

## Full file at head: THIRD_PARTY_NOTICES.md
```
    1| # Third-Party Notices
    2| 
    3| **Status:** T086 exact-version dependency license/provenance review  
    4| **Scope:** direct dependencies intentionally selected for Ascout M1, bound to the current committed manifest and lockfile.
    5| 
    6| This file records the exact direct third-party packages selected by Ascout and the evidence used to bind those selections to the committed lockfile. Exact transitive versions, registry locations, integrity digests, and license metadata are recorded in `package-lock.json` where npm provides those fields.
    7| 
    8| ## Current candidate binding
    9| 
   10| T086 revalidated this ledger against canonical `main` at `a9bae09a71b4ff92097182a8d97f5ff6a0511603`.
   11| 
   12| - `package.json` blob: `e5d99fcd1bb87fa3adec2629d949bde933000bf7`
   13| - `package-lock.json` blob: `e51f0bddb953235c1a391718eabfab5a6c680832`
   14| - Product runtime dependency count: 1 (`cross-spawn@7.0.6`)
   15| - Direct development dependency count: 6 (`@types/node`, `@vitest/coverage-v8`, `jest`, `typescript`, `vite`, `vitest`)
   16| - Direct manifest/lockfile reconciliation: complete; no direct dependency is omitted from this notice ledger.
   17| 
   18| The committed npm lockfile is the canonical machine-readable graph for this candidate. The T086 review does not upgrade dependencies, regenerate the lockfile, alter package identity, publish to npm, or claim that a point-in-time security audit is permanent.
   19| 
   20| ## Lock generation evidence
   21| 
   22| - Evidence branch: `evidence/t003-lockgen-2026-08-22` (the date component is the Asia/Riyadh local date; the corresponding GitHub Actions timestamps are on 2026-08-21 UTC).
   23| - Evidence commit containing the generated lockfile: `81e2850e06a097abed5a7566aded39fceb330800`
   24| - Original generated `package-lock.json` blob: `751fdf89c10d26a1875844626ad6c336b28d051b`
   25| - GitHub Actions generation run: `32535056565`
   26| - Runner OS: Ubuntu 24.04
   27| - Node: `22.0.0`
   28| - npm resolver: `10.9.4`
   29| - Generation command: `npm install --package-lock-only --ignore-scripts --audit=false --fund=false`
   30| - Reproduction check: `npm ci --ignore-scripts --audit=false --fund=false` — PASS
   31| - Exact direct-resolution check — PASS
   32| - `npm ls --all` — exited successfully; its tree truthfully reports platform-, peer-, and engine-inapplicable optional dependencies as `UNMET OPTIONAL DEPENDENCY` rather than treating them as required install failures.
   33| - Tool execution on Node 22.0.0: TypeScript `6.0.3`, Vite `6.4.3`, Vitest `4.1.10` — PASS
   34| - Generation-time security check: `npm audit --package-lock-only --audit-level=high` reported `found 0 vulnerabilities`.
   35| 
   36| ### Node 22.0.0 engine-strict verification
   37| 
   38| A follow-up evidence run `32535678363` used the same package manifest and unchanged lockfile blob on Node `22.0.0` with npm `10.9.4` and added an engine-strict installation gate:
   39| 
   40| - `npm ci --engine-strict --ignore-scripts --audit=false --fund=false` — PASS
   41| - `@napi-rs/lzma-linux-x64-gnu@1.5.1`, an optional dependency of `rollup@4.62.5` whose own engine range starts at Node 22.20, was omitted by npm on Node 22.0.0 as an inapplicable optional dependency.
   42| - The workflow asserted that this optional package was absent after the engine-strict install.
   43| - Vite `6.4.3` executed on Node `22.0.0` after that install — PASS.
   44| - Vitest `4.1.10` executed on Node `22.0.0` after that install — PASS.
   45| - The follow-up audit again reported `found 0 vulnerabilities` for the resolved lockfile graph.
   46| 
   47| The stricter engine range of an omitted optional package therefore does not redefine Ascout's Node `>=22` support floor. The evidence above is deliberately scoped to the tested Ubuntu x64 environment and does not claim an untested platform result.
   48| 
   49| Security/audit results are evidence for the specific resolved graph at the cited runs; they are not permanent security claims.
   50| 
   51| ## T086 license/provenance reconciliation
   52| 
   53| All seven direct packages declared by the current candidate are represented below at their exact locked versions. The current direct set contains Apache-2.0 and MIT licenses only. No direct copyleft, source-available, non-commercial, field-of-use, database, or data-license restriction was identified in the manifest/lockfile evidence reviewed for T086.
   54| 
   55| This conclusion is scoped to the exact direct package versions below. Transitive packages remain separately represented by the committed lockfile and may use other permissive SPDX licenses. A future dependency/version change requires a fresh provenance/license reconciliation before release claims are updated.
   56| 
   57| ## Direct dependencies
   58| 
   59| ### `cross-spawn` 7.0.6
   60| 
   61| - Role: product runtime dependency
   62| - License: MIT
   63| - Upstream: `moxystudio/node-cross-spawn`, tag `v7.0.6`
   64| - Registry tarball: `https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz`
   65| - SRI: `sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==`
   66| 
   67| ### `@types/node` 22.20.1
   68| 
   69| - Role: development-only Node.js type declarations aligned to the Node 22 support floor
   70| - License: MIT
   71| - Upstream: `DefinitelyTyped/DefinitelyTyped`, package path `types/node`
   72| - Registry tarball: `https://registry.npmjs.org/@types/node/-/node-22.20.1.tgz`
   73| - SRI: `sha512-EANqOCF9QFyra+4pfxUcX9STKJpCLjMbObVzljIJomAWSnuSIEAvyzEU53GaajbXJEgdh0iEcPL+DGvpUd4k1Q==`
   74| 
   75| ### `@vitest/coverage-v8` 4.1.11
   76| 
   77| - Role: development-only V8 coverage provider used by the Vitest integration and changed-code exercise tests
   78| - License: MIT
   79| - Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/coverage-v8`
   80| - Registry tarball: `https://registry.npmjs.org/@vitest/coverage-v8/-/coverage-v8-4.1.11.tgz`
   81| - SRI: `sha512-8MVGEFnJIcdGjcbfKmeq8z0pZHH0JlVtoVZH9Q/qwUp6wyFnEJUBMrw9DCaj+ra3vShGmhavjalMIhPNxZAUcw==`
   82| 
   83| ### `jest` 30.4.2
   84| 
   85| - Role: development-only Jest runner used to qualify Ascout's supported Jest integration
   86| - License: MIT
   87| - Upstream: `jestjs/jest`, tag `v30.4.2`
   88| - Registry tarball: `https://registry.npmjs.org/jest/-/jest-30.4.2.tgz`
   89| - SRI: `sha512-Yi1jqNC/Oq0N4hBgNH/YvBpP1P57QqundgytzYqy3yqAa7NZPNjSoi4SGbRAXDMdBzNE6xBCi5U7RgfrvMEUVQ==`
   90| 
   91| ### `typescript` 6.0.3
   92| 
   93| - Role: development-only compiler/typechecker
   94| - License: Apache-2.0
   95| - Upstream: `microsoft/TypeScript`, tag `v6.0.3`
   96| - Registry tarball: `https://registry.npmjs.org/typescript/-/typescript-6.0.3.tgz`
   97| - SRI: `sha512-y2TvuxSZPDyQakkFRPZHKFm+KKVqIisdg9/CZwm9ftvKXLP8NRWj38/ODjNbr43SsoXqNuAisEf1GdCxqWcdBw==`
   98| 
   99| ### `vite` 6.4.3
  100| 
  101| - Role: development-only peer/runtime substrate selected for Vitest while preserving the Ascout Node `>=22` floor
  102| - License: MIT
  103| - Upstream: `vitejs/vite`, tag `v6.4.3`, package path `packages/vite`
  104| - Registry tarball: `https://registry.npmjs.org/vite/-/vite-6.4.3.tgz`
  105| - SRI: `sha512-NTKlcQjlAK7MlQoyb6LgaqHc8sso/pVyUJYWMws3jg21uTJw/LddqIFPcPqP6PzpgbIcZyKI85sFE4HBrQDA8A==`
  106| 
  107| ### `vitest` 4.1.11
  108| 
  109| - Role: development-only test runner
  110| - License: MIT
  111| - Upstream: `vitest-dev/vitest`, tag `v4.1.11`, package path `packages/vitest`
  112| - Registry tarball: `https://registry.npmjs.org/vitest/-/vitest-4.1.11.tgz`
  113| - SRI: `sha512-fhACrNXUidIbGSBr5FlbuBkO7VWC1ZyLl0DO4CU2DrQoAPxX84Ysxs+HeGQpii5lZWV1Q4gBZTTu49mF+A6Edw==`
  114| 
  115| ## Transitive dependencies
  116| 
  117| `package-lock.json` is the canonical machine-readable record for the exact resolved transitive graph used by this revision, including registry `resolved` URLs, SRI `integrity` values, and license metadata where npm records it. Optional entries can legitimately remain recorded even when npm omits them on a particular platform or Node version.
  118| 
  119| The T086 review does not treat process isolation, development-only status, or npm registry availability as a substitute for license terms. It also does not assume that a permissive direct package makes every possible future bundled artifact attribution-free. The T082 package-content gate proves the current Ascout tarball surface separately; any future bundling/vendor change must re-evaluate redistribution and notice obligations.
  120| 
  121| This file does not replace any third-party license text or attribution that a future packaged distribution is legally required to carry.
  122| 
  123| ## Donor snapshot — google/artemis (ARTEMIS A0)
  124| 
  125| - Upstream: `https://github.com/google/artemis`
  126| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  127| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  128| - License: Apache-2.0
  129| - Ascout paths: `vendor/google-artemis/**` plus separately reviewed adapters
  130| - Use type: copied + adapted, Class C provenance
  131| - Snapshot content: complete repository snapshot at the exact commit (796 blob paths)
  132| - Notice preservation: donor LICENSE, copyright headers, and notice material preserved inside the immutable snapshot; no modifications inside the snapshot
  133| - Runtime authority: none granted by source presence; activation requires separate phased authorization and qualification
  134| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
  135| 
  136| ## Donor snapshot — google/artemis (ARTEMIS A13 release admission)
  137| 
  138| - Upstream: `https://github.com/google/artemis`
  139| - Pinned commit: `371aa6df56880643da57b30da936e9812fb0ec66`
  140| - Pinned tree: `697c3fe48b51b8453938989f383b4a8471a4f5a1`
  141| - License: Apache-2.0
  142| - Release scope: contract, adapter, evidence, and documentation layers under `vendor/google-artemis/**`, `src/assurance/engines/mobile-artemis/**`, `python/ascout_mobile_bridge/**`, `schemas/mobile-artemis/**`, `docs/mobile/**`
  143| - Phases admitted: ARTEMIS-A0 through ARTEMIS-A12 closed canonically; A13 gates recorded in `docs/mobile/artemis-a13-release.md`
  144| - Donor telemetry: off by default; no telemetry destination admitted
  145| - Runtime authority: none granted by source presence or by release admission
  146| - Provenance record: `docs/mobile/artemis-a0-provenance.json`
```

## Full file at head: package.json
```
    1| {
    2|   "name": "@thehalfmoon/ascout",
    3|   "version": "0.1.0",
    4|   "private": true,
    5|   "description": "Verify everything AI ships.",
    6|   "license": "Apache-2.0",
    7|   "type": "module",
    8|   "files": [
    9|     "dist"
   10|   ],
   11|   "bin": {
   12|     "ascout": "./dist/cli.js"
   13|   },
   14|   "engines": {
   15|     "node": ">=22"
   16|   },
   17|   "scripts": {
   18|     "build": "tsc -p tsconfig.json",
   19|     "typecheck": "tsc -p tsconfig.json --noEmit",
   20|     "test": "vitest run"
   21|   },
   22|   "dependencies": {
   23|     "cross-spawn": "7.0.6",
   24|     "playwright": "1.63.0"
   25|   },
   26|   "devDependencies": {
   27|     "@types/node": "22.20.1",
   28|     "@vitest/coverage-v8": "4.1.11",
   29|     "jest": "30.4.2",
   30|     "typescript": "6.0.3",
   31|     "vite": "6.4.3",
   32|     "vitest": "4.1.11"
   33|   }
   34| }
```

## Full file at head: tests/vitest-check.integration.test.ts
```
    1| import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
    2| import { tmpdir } from "node:os";
    3| import { basename, join, resolve } from "node:path";
    4| import { spawnSync } from "node:child_process";
    5| 
    6| import { describe, expect, it } from "vitest";
    7| 
    8| import { runCheck } from "../src/check.js";
    9| import { normalizeLcovLineCoverage } from "../src/coverage/lcov.js";
   10| import { UNSAFE_SELECTION_LIMITATION, validateReceiptSemantics } from "../src/receipt/model.js";
   11| import { SELECTION_COUNTS_NOT_OBSERVED_LIMITATION } from "../src/selection.js";
   12| import { writePackageNodeCommandShim } from "./helpers/native-command-shim.js";
   13| 
   14| function run(root: string, file: string, argv: readonly string[]): void {
   15|   const result = spawnSync(file, argv, { cwd: root, encoding: "utf8" });
   16|   if (result.status !== 0) {
   17|     throw new Error(`${file} ${argv.join(" ")} failed: ${result.stderr || result.stdout}`);
   18|   }
   19| }
   20| 
   21| function initializeFixture(): string {
   22|   const root = mkdtempSync(join(tmpdir(), "ascout-t051-check-"));
   23|   mkdirSync(join(root, "src"), { recursive: true });
   24|   mkdirSync(join(root, "tests"), { recursive: true });
   25|   cpSync(resolve("node_modules"), join(root, "node_modules"), { recursive: true });
   26|   const binRoot = join(root, "node_modules", ".bin");
   27|   rmSync(binRoot, { recursive: true, force: true });
   28|   writePackageNodeCommandShim(binRoot, "vitest", "../vitest/vitest.mjs");
   29|   writeFileSync(join(root, ".gitignore"), ".ascout/\nnode_modules/\n");
   30|   writeFileSync(
   31|     join(root, "package.json"),
   32|     JSON.stringify({
   33|       name: "t051-vitest-check-fixture",
   34|       private: true,
   35|       type: "module",
   36|       devDependencies: { vitest: "4.1.11", "@vitest/coverage-v8": "4.1.11" },
   37|     }),
   38|   );
   39|   writeFileSync(join(root, "vitest.config.mjs"), "export default { test: { globals: true } };\n");
   40|   writeFileSync(join(root, "src", "used.js"), "export function used() { return 2; }\n");
   41|   writeFileSync(join(root, "src", "unused.js"), "export function unused() { return 3; }\n");
   42|   writeFileSync(
   43|     join(root, "tests", "used.test.js"),
   44|     'import { used } from "../src/used.js";\ntest("used", () => { expect(used()).toBe(2); });\n',
   45|   );
   46|   writeFileSync(
   47|     join(root, "tests", "unused.test.js"),
   48|     'import { unused } from "../src/unused.js";\ntest("unused", () => { expect(unused()).toBe(3); });\n',
   49|   );
   50|   run(root, "git", ["init", "-q"]);
   51|   run(root, "git", ["config", "user.name", "Ascout T051 Fixture"]);
   52|   run(root, "git", ["config", "user.email", "t051@example.invalid"]);
   53|   run(root, "git", ["add", "."]);
   54|   run(root, "git", ["commit", "-qm", "baseline"]);
   55|   writeFileSync(join(root, "src", "used.js"), "export function used() { return 1 + 1; }\n");
   56|   return root;
   57| }
   58| 
   59| type ControlledLcovMode =
   60|   | "absent"
   61|   | "resolved_gap"
   62|   | "malformed"
   63|   | "path_unsafe"
   64|   | "incomplete"
   65|   | "invalid_taken";
   66| 
   67| const FAIL_CLOSED_MODES = ["malformed", "path_unsafe", "incomplete", "invalid_taken"] as const;
   68| 
   69| function controlledLcov(mode: ControlledLcovMode): string {
   70|   switch (mode) {
   71|     case "absent":
   72|       return "SF:src/used.js\nDA:1,1\nend_of_record\n";
   73|     case "resolved_gap":
   74|       return "SF:src/used.js\nDA:1,1\nBRDA:1,0,0,1\nBRDA:1,0,1,0\nend_of_record\n";
   75|     case "malformed":
   76|       return "SF:src/used.js\nDA:1,1\nBRDA:1,0,0\nend_of_record\n";
   77|     case "path_unsafe":
   78|       return "SF:../outside.js\nDA:1,1\nBRDA:1,0,0,1\nend_of_record\n";
   79|     case "incomplete":
   80|       return "SF:src/used.js\nDA:1,1\nBRDA:1,0,0,1\n";
   81|     case "invalid_taken":
   82|       return "SF:src/used.js\nDA:1,1\nBRDA:1,0,0,invalid\nend_of_record\n";
   83|   }
   84| }
   85| 
   86| function initializeControlledBranchFixture(mode: ControlledLcovMode): string {
   87|   const root = mkdtempSync(join(tmpdir(), `ascout-t103-vitest-${mode}-`));
   88|   mkdirSync(join(root, "src"), { recursive: true });
   89|   mkdirSync(join(root, "node_modules", "vitest"), { recursive: true });
   90|   mkdirSync(join(root, "node_modules", "@vitest", "coverage-v8"), { recursive: true });
   91|   mkdirSync(join(root, "node_modules", "fake-vitest"), { recursive: true });
   92| 
   93|   writeFileSync(join(root, ".gitignore"), ".ascout/\nnode_modules/\n");
   94|   writeFileSync(
   95|     join(root, "package.json"),
   96|     JSON.stringify({
   97|       name: `t103-vitest-${mode}`,
   98|       private: true,
   99|       type: "module",
  100|       devDependencies: { vitest: "4.1.10", "@vitest/coverage-v8": "4.1.10" },
  101|     }),
  102|   );
  103|   writeFileSync(
  104|     join(root, "node_modules", "vitest", "package.json"),
  105|     JSON.stringify({ name: "vitest", version: "4.1.10" }),
  106|   );
  107|   writeFileSync(
  108|     join(root, "node_modules", "@vitest", "coverage-v8", "package.json"),
  109|     JSON.stringify({ name: "@vitest/coverage-v8", version: "4.1.10" }),
  110|   );
  111| 
  112|   const fakeRunner = [
  113|     'import { mkdirSync, writeFileSync } from "node:fs";',
  114|     'import { dirname } from "node:path";',
  115|     'const output = process.argv.find((arg) => arg.startsWith("--outputFile="))?.slice("--outputFile=".length);',
  116|     'const coverageDir = process.argv.find((arg) => arg.startsWith("--coverage.reportsDirectory="))?.slice("--coverage.reportsDirectory=".length);',
  117|     'if (!output || !coverageDir) process.exit(64);',
  118|     'mkdirSync(dirname(output), { recursive: true });',
  119|     'mkdirSync(coverageDir, { recursive: true });',
  120|     'writeFileSync(output, JSON.stringify({ numTotalTests: 1, testResults: [] }));',
  121|     `writeFileSync(coverageDir + "/lcov.info", ${JSON.stringify(controlledLcov(mode))});`,
  122|   ].join("\n");
  123|   writeFileSync(join(root, "node_modules", "fake-vitest", "index.mjs"), `${fakeRunner}\n`);
  124|   writePackageNodeCommandShim(join(root, "node_modules", ".bin"), "vitest", "../fake-vitest/index.mjs");
  125| 
  126|   writeFileSync(join(root, "src", "used.js"), "export function used() { return 2; }\n");
  127|   run(root, "git", ["init", "-q"]);
  128|   run(root, "git", ["config", "user.name", "Ascout T103 Fixture"]);
  129|   run(root, "git", ["config", "user.email", "t103@example.invalid"]);
  130|   run(root, "git", ["add", "."]);
  131|   run(root, "git", ["commit", "-qm", "baseline"]);
  132|   writeFileSync(join(root, "src", "used.js"), "export function used() { return 1 + 1; }\n");
  133|   return root;
  134| }
  135| 
  136| describe("T051 runCheck Vitest integration", () => {
  137|   it("runs project-local related Vitest and binds JSON plus LCOV while remaining fail-closed before widening/exercise", async () => {
  138|     const root = initializeFixture();
  139|     try {
  140|       const outcome = await runCheck(root);
  141|       const receipt = outcome.receipt;
  142|       expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  143|       expect(receipt.stability).toBe("stable");
  144|       expect(receipt.selection.mode).toBe("native_related");
  145|       expect(receipt.selection.passes).toHaveLength(1);
  146|       expect(receipt.selection.limitations).not.toContain(UNSAFE_SELECTION_LIMITATION);
  147|       expect(receipt.selection.limitations).toContain(SELECTION_COUNTS_NOT_OBSERVED_LIMITATION);
  148|       expect(receipt.selection.selected_test_count).toBe(1);
  149|       expect(receipt.selection.deselected_test_count).toBeNull();
  150|       expect(receipt.selection.total_test_count).toBeNull();
  151|       expect(receipt.summary.completeness).toBe("complete");
  152|       expect(receipt.summary.exit_code).toBe(0);
  153| 
  154|       const task = receipt.tasks.find((candidate) => candidate.task_type === "test");
  155|       expect(task).toMatchObject({
  156|         status: "PASS",
  157|         tool_name: "vitest",
  158|         tool_version: "4.1.11",
  159|         execution_admission: "normal",
  160|       });
  161|       expect(task?.argv).toContain("related");
  162|       expect(task?.argv).toContain("src/used.js");
  163|       expect(task?.argv).not.toContain("src/unused.js");
  164| 
  165|       const testEvidence = receipt.evidence.filter((item) => item.task_id === "test");
  166|       expect(testEvidence.some((item) => item.kind === "test_result")).toBe(true);
  167|       expect(testEvidence.some((item) => item.kind === "coverage")).toBe(true);
  168| 
  169|       const resultArtifact = receipt.artifacts.find((artifact) => artifact.artifact_id === "test.vitest-results");
  170|       const coverageArtifact = receipt.artifacts.find((artifact) => artifact.artifact_id === "test.lcov");
  171|       expect(resultArtifact?.relative_run_path).toBe("raw/test/vitest-results.json");
  172|       expect(coverageArtifact?.relative_run_path).toBe("raw/test/coverage/lcov.info");
  173|       expect(resultArtifact && existsSync(join(root, ".ascout", "runs", receipt.run.run_id, resultArtifact.relative_run_path))).toBe(true);
  174|       expect(coverageArtifact && existsSync(join(root, ".ascout", "runs", receipt.run.run_id, coverageArtifact.relative_run_path))).toBe(true);
  175| 
  176|       const resultJson = JSON.parse(
  177|         readFileSync(join(root, ".ascout", "runs", receipt.run.run_id, resultArtifact!.relative_run_path), "utf8"),
  178|       ) as { testResults?: readonly { name?: string }[] };
  179|       const selectedFiles = (resultJson.testResults ?? []).map(({ name }) => name === undefined ? "" : basename(name));
  180|       expect(selectedFiles).toContain("used.test.js");
  181|       expect(selectedFiles).not.toContain("unused.test.js");
  182| 
  183|       const lcovText = readFileSync(
  184|         join(root, ".ascout", "runs", receipt.run.run_id, coverageArtifact!.relative_run_path),
  185|         "utf8",
  186|       );
  187|       const normalized = normalizeLcovLineCoverage(lcovText, root);
  188|       expect(normalized.outcome).toBe("resolved");
  189|       if (normalized.outcome === "resolved") {
  190|         expect(normalized.points.some((point) => point.path === "src/used.js" && point.count > 0)).toBe(true);
  191|       }
  192|     } finally {
  193|       rmSync(root, { recursive: true, force: true });
  194|     }
  195|   }, 120_000);
  196| });
  197| 
  198| describe("T103 runCheck Vitest branch receipt integration", () => {
  199|   it("keeps optional branch fields absent when LCOV has genuine line-only coverage", async () => {
  200|     const root = initializeControlledBranchFixture("absent");
  201|     try {
  202|       const { receipt } = await runCheck(root);
  203|       expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  204|       expect(receipt.exercise.records).toEqual([
  205|         {
  206|           path: "src/used.js",
  207|           line: 1,
  208|           state: "EXERCISED",
  209|           execution_count: 1,
  210|           source_task_ids: ["test"],
  211|         },
  212|       ]);
  213|       expect(receipt.exercise.branch_records).toBeUndefined();
  214|       expect(receipt.exercise.exercised_branches).toBeUndefined();
  215|       expect(receipt.exercise.not_exercised_branches).toBeUndefined();
  216|       expect(receipt.exercise.unresolved_branches).toBeUndefined();
  217|       expect(receipt.exercise.changed_files_with_zero_exercised_branches).toBeUndefined();
  218|       expect(receipt.summary).toMatchObject({ completeness: "complete", exit_code: 0 });
  219|     } finally {
  220|       rmSync(root, { recursive: true, force: true });
  221|     }
  222|   }, 15_000);
  223| 
  224|   it("publishes resolved branch evidence and makes a branch-only miss exit 4", async () => {
  225|     const root = initializeControlledBranchFixture("resolved_gap");
  226|     try {
  227|       const { receipt } = await runCheck(root);
  228|       expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  229|       expect(receipt.exercise.records).toEqual([
  230|         {
  231|           path: "src/used.js",
  232|           line: 1,
  233|           state: "EXERCISED",
  234|           execution_count: 1,
  235|           source_task_ids: ["test"],
  236|         },
  237|       ]);
  238|       expect(receipt.exercise.branch_records).toEqual([
  239|         {
  240|           path: "src/used.js",
  241|           line: 1,
  242|           block_id: "0",
  243|           branch_id: "0",
  244|           taken: 1,
  245|           state: "EXERCISED",
  246|         },
  247|         {
  248|           path: "src/used.js",
  249|           line: 1,
  250|           block_id: "0",
  251|           branch_id: "1",
  252|           taken: 0,
  253|           state: "NOT_EXERCISED",
  254|         },
  255|       ]);
  256|       expect(receipt.exercise).toMatchObject({
  257|         exercised_branches: 1,
  258|         not_exercised_branches: 1,
  259|         unresolved_branches: 0,
  260|         changed_files_with_zero_exercised_branches: 0,
  261|       });
  262|       expect(receipt.summary).toMatchObject({ completeness: "materially_incomplete", exit_code: 4 });
  263|     } finally {
  264|       rmSync(root, { recursive: true, force: true });
  265|     }
  266|   }, 15_000);
  267| 
  268|   it.each(FAIL_CLOSED_MODES)("fails closed for %s branch normalization instead of manufacturing empty evidence", async (mode) => {
  269|     const root = initializeControlledBranchFixture(mode);
  270|     try {
  271|       const { receipt } = await runCheck(root);
  272|       const testTask = receipt.tasks.find(({ task_type }) => task_type === "test");
  273|       expect(testTask).toMatchObject({ status: "ERROR", reason_code: "vitest_evidence_invalid" });
  274|       expect(receipt.exercise.branch_records).toBeUndefined();
  275|       expect(receipt.exercise.exercised_branches).toBeUndefined();
  276|       expect(receipt.exercise.not_exercised_branches).toBeUndefined();
  277|       expect(receipt.exercise.unresolved_branches).toBeUndefined();
  278|       expect(receipt.exercise.changed_files_with_zero_exercised_branches).toBeUndefined();
  279|       expect(receipt.summary).toMatchObject({ completeness: "unknown_due_to_error", exit_code: 2 });
  280|       expect(validateReceiptSemantics(receipt)).toEqual({ valid: true, issues: [] });
  281|     } finally {
  282|       rmSync(root, { recursive: true, force: true });
  283|     }
  284|   }, 15_000);
  285| });
```
