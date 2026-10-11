You are performing a code review in Alibaba OpenCodeReview (OCR) delegation mode. OCR has already selected the files and supplied the review rules below; you perform the review.

Repository: the current working directory (a Git repository).
Review range: __BASE__..__HEAD__
Files selected by OCR: src/receipt-store.ts

Instructions:
1. Read the change with: git diff __BASE__..__HEAD__ -- src/receipt-store.ts  (you may also read the full file at __HEAD__ with: git show __HEAD__:src/receipt-store.ts).
2. Review ONLY changed (+) lines, focusing on correctness, security, performance, error handling, concurrency, and maintainability, guided by the OCR rules below.
3. Classify each issue: High (obvious bugs, security issues, data loss, clear mistakes) or Medium (reasonable concerns). Discard Low-severity issues and nitpicks entirely.
4. Do not modify any files. Do not read anything outside this repository.
5. Reply with ONLY a JSON object, no prose, in exactly this shape:
{"comments":[{"path":"src/receipt-store.ts","start_line":<int>,"end_line":<int>,"category":"bug|security|performance|maintainability|other","severity":"high|medium","content":"<explanation>"}]}
Line numbers refer to the file at __HEAD__. If there are no High or Medium issues, reply {"comments":[]}.

OCR review rules for src/receipt-store.ts:
__RULES__
