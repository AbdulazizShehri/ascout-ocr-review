"""Fail-closed machine checks for exact-range OCR review artifacts.

Successful validation is evidence of completion, never an independent PR approval.
"""
import json
import re
import sys


def check(result, base, head):
    reasons = []
    if not isinstance(result, dict):
        return ["output must be a JSON object"]
    if result.get("status") != "completed":
        reasons.append("OCR status is not completed")
    manifest = result.get("manifest")
    if not isinstance(manifest, dict):
        return reasons + ["missing manifest"]
    source = manifest.get("input")
    if not isinstance(source, dict):
        reasons.append("missing manifest.input")
        source = {}
    exact_range = source.get("exact_range")
    text = json.dumps(exact_range, sort_keys=True)
    if not (
        re.fullmatch(r"[0-9a-f]{40}", base)
        and re.fullmatch(r"[0-9a-f]{40}", head)
        and base in text and head in text
    ):
        reasons.append("manifest does not bind the expected full base and head SHAs")
    cov = manifest.get("coverage")
    if not isinstance(cov, dict):
        return reasons + ["missing manifest.coverage"]
    selected, completed, failed = (cov.get(name) for name in ("selected", "completed", "failed"))
    if not all(isinstance(value, list) for value in (selected, completed, failed)):
        reasons.append("missing or malformed coverage arrays")
    elif not selected or len(completed) != len(selected) or failed:
        reasons.append("review coverage is not complete")
    summary = result.get("summary")
    if not isinstance(summary, dict):
        reasons.append("missing token/budget summary")
    elif summary.get("budget_exceeded") is True:
        reasons.append("token budget was exceeded")
    warnings = result.get("warnings") or []
    if not isinstance(warnings, list):
        reasons.append("malformed warnings")
    elif any(
        w == "token_budget_reached"
        or isinstance(w, dict) and w.get("type") in ("token_budget_reached", "budget_exceeded")
        for w in warnings
    ):
        reasons.append("token budget stop in warnings")
    comments = result.get("comments")
    if comments is not None and (
        not isinstance(comments, list) or not all(isinstance(c, dict) for c in comments)
    ):
        reasons.append("malformed review comments")
    return reasons


def main(argv):
    if len(argv) != 4:
        print("usage: check-review.py REVIEW_JSON BASE_SHA HEAD_SHA", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as handle:
            result = json.load(handle)
    except (OSError, ValueError) as exc:
        print(f"::error::OCR result is unreadable: {exc}", file=sys.stderr)
        return 1
    errors = check(result, argv[2], argv[3])
    print("## OCR exact-range review validation")
    print(f"- requested base: `{argv[2]}`")
    print(f"- requested head: `{argv[3]}`")
    print(f"- OCR status: {result.get('status') if isinstance(result, dict) else 'invalid'}")
    print(f"- comments: {len(result.get('comments') or []) if isinstance(result, dict) else 'unknown'}")
    print(f"- machine gate: {'PASS' if not errors else 'FAIL'}")
    for error in errors:
        print(f"- failure: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
