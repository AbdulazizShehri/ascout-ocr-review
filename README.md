# ascout-ocr-review

Independent Alibaba OpenCodeReview (OCR) harness for [Ascout](https://github.com/TheHalfMoon/Ascout). The hosted runner is intended to use no paid compute. Cloud model calls are **not automatically free**: confirm provider-level billing controls before using Qwen.

## Zero-cost guardrails

- **Region/model:** Only `dashscope-cn` (China/Beijing) with `qwen3-coder-plus` is admitted to the Alibaba path. Singapore/international DashScope is intentionally disabled because Alibaba's published new-user free quota applies only in Beijing.
- **Console prerequisite:** The person operating Model Studio must check that the model still has a valid free quota and **Free Quota Only is ACTIVE**, not merely being enabled. Dispatching with Alibaba requires the explicit `free_quota_only_confirmed=true` input. The workflow cannot verify this third-party billing setting.
- **Secret:** Add `DASHSCOPE_API_KEY` in repository Actions secrets. It is read only at runtime with `api_key_cmd`; never paste it into GitHub input text, chat, code, or the OCR config.
- **Token budget:** Default `100000`, maximum `150000` per OCR invocation. `--max-tokens-budget` is a **work-limiting control, not a financial ceiling**; in-flight calls can exceed it. Neither token budget nor GitHub job timeout guarantees zero charges. `Free Quota Only` is the cost-stop control.
- **Independent review:** Both `qualify` and `review` dispatches run the *same-run* planted+clean qualification first, under the same provider/model/budget as the subsequent review. A failed, missing, incomplete, timed-out, budget-stopped, or pending-adjudication qualification exits nonzero. No Ascout review runs afterward.
- **Egress:** Before `review` reads an Ascout diff through OCR, pinned/checksum-verified gitleaks scans the exact requested commit range. Findings fail closed. Reviews run only on immutable full-SHA ranges. The Ascout repository is public; this is still external source transmission.
- **Local alternative:** `ollama-local` does not use a cloud API key or transmit source to Alibaba. It must independently pass the same qualification; it is not presumed qualified from a successful workflow job.

## How to use

1. Read [Alibaba Model Studio free-quota rules](https://help.aliyun.com/en/model-studio/new-free-quota), [model pricing and regional scope](https://help.aliyun.com/en/model-studio/model-pricing), and the data-handling terms.
2. Activate Model Studio in **China (Beijing)**, verify availability of the free quota for `qwen3-coder-plus`, and enable **Free Quota Only**. Verify the setting is **ACTIVE** before dispatch; it can take time to take effect.
3. Set the secret without exposing it in chat:

   ```bash
   gh secret set DASHSCOPE_API_KEY -R AbdulazizShehri/ascout-ocr-review
   ```

4. From Actions → **OCR review**, select `qualify` to run the preregistered planted/clean control. Choose `dashscope-cn`, `qwen3-coder-plus`, and confirm the active billing protection. Do not interpret a workflow success as an approval.
5. For a specific Ascout PR, select `review` and supply **both full 40-character commit SHAs** for the applicable exact ancestor range. This always repeats qualification within the same run, then scans secrets, then invokes OCR on the requested range.
6. Retrieve the workflow run and attached JSON artifact; verify the exact reviewed head, coverage, model, budget state, and findings. Apply Ascout governance and other required tests/reviews before any Ascout PR merge.

`harness/ground-truth.json` is preregistered and unchanged. In its frozen rule, a clean-control comment requires manual adjudication. The automatic gate therefore passes only when the clean control has **zero** comments; one clean comment remains `PROVISIONAL_PASS_PENDING_CLEAN_ADJUDICATION` and blocks the workflow. The scorer never waives missing defects, partial coverage, or budget exhaustion.

Offline regression tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v`. They do not access a model, an account, or a network.

## Non-claims

A completed workflow is not a PR approval. A comment-free review is not proof of correctness. Neither `Free Quota Only` nor a token budget proves no earlier charges occurred. The workflow **cannot** establish the current status of your personal Alibaba subscription or free-quota balance.
