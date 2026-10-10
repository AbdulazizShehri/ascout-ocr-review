"""Fail-closed OCR qualification against preregistered ground truth.

A nonzero exit is mandatory for missing/incomplete evidence, budget exhaustion,
or a clean control requiring human adjudication. No result here is a PR approval.
"""
import json
import sys


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else {"status": "invalid-json-object"}
    except (OSError, ValueError) as exc:
        return {"status": f"unreadable: {exc}"}


def coverage(result):
    manifest = result.get("manifest")
    cov = (manifest or {}).get("coverage") if isinstance(manifest, dict) else None
    if not isinstance(cov, dict):
        return (0, 0, 1)
    selected, completed, failed = (cov.get(key) for key in ("selected", "completed", "failed"))
    if not all(isinstance(part, list) for part in (selected, completed, failed)):
        return (0, 0, 1)
    return (len(selected), len(completed), len(failed))


def comments(result):
    found = result.get("comments")
    if found is None:
        return []
    return found if isinstance(found, list) and all(isinstance(c, dict) for c in found) else None


def has_budget_stop(result):
    summary = result.get("summary")
    if not isinstance(summary, dict):
        return True
    if summary.get("budget_exceeded") is True:
        return True
    warnings = result.get("warnings") or []
    if not isinstance(warnings, list):
        return True
    return any(
        w == "token_budget_reached"
        or isinstance(w, dict) and w.get("type") in ("token_budget_reached", "budget_exceeded")
        for w in warnings
    )


def terminal_complete(result):
    # With a run manifest OCR sets status to manifest.terminal_state, one of
    # complete | partial | failed | skipped (open-code-review v1.12.13).
    manifest = result.get("manifest")
    return (
        result.get("status") == "complete"
        and isinstance(manifest, dict)
        and manifest.get("terminal_state") == "complete"
    )


def complete(result):
    return (
        terminal_complete(result)
        and coverage(result) == (1, 1, 0)
        and comments(result) is not None
        and not has_budget_stop(result)
    )


def lines(comment):
    found = []
    for key in ("line", "start_line", "end_line", "startLine", "endLine", "new_line"):
        value = comment.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            found.append(value)
    loc = comment.get("location") or comment.get("range") or {}
    if isinstance(loc, dict):
        found.extend(v for v in loc.values() if isinstance(v, int) and not isinstance(v, bool))
    return found


def main(argv):
    if len(argv) != 4:
        print("usage: score.py TRUTH PLANTED CLEAN", file=sys.stderr)
        return 2
    truth, planted, clean = (load(path) for path in argv[1:])
    try:
        defects = truth["planted"]
        tolerance = truth["line_tolerance"]
        assert isinstance(defects, list) and defects
        assert isinstance(tolerance, int) and tolerance >= 0
        assert all(isinstance(d["line"], int) and d["keywords"] for d in defects)
    except (KeyError, TypeError, AssertionError):
        print("invalid or missing preregistered ground truth", file=sys.stderr)
        return 2

    findings = comments(planted) or []
    clean_findings = comments(clean)
    matches = {}
    for defect in defects:
        hit = False
        for comment in findings:
            text = " ".join(str(comment.get(key, "")) for key in
                            ("content", "existing_code", "suggestion_code")).lower()
            first, last = comment.get("start_line"), comment.get("end_line")
            near = any(abs(line - defect["line"]) <= tolerance for line in lines(comment))
            if isinstance(first, int) and isinstance(last, int):
                near = near or first <= defect["line"] <= last
            if near and any(word.lower() in text for word in defect["keywords"]):
                hit = True
                break
        matches[defect["id"]] = hit

    planted_ok, clean_ok = complete(planted), complete(clean)
    any_clean = clean_findings is not None and len(clean_findings) > 0
    meets_auto = planted_ok and clean_ok and all(matches.values()) and not any_clean
    pending_adjudication = (
        planted_ok and clean_ok and all(matches.values())
        and clean_findings is not None and len(clean_findings) == 1
    )
    verdict = (
        "PASS_AUTOMATIC_CRITERIA" if meets_auto
        else "PROVISIONAL_PASS_PENDING_CLEAN_ADJUDICATION" if pending_adjudication
        else "NOT_QUALIFIED"
    )
    result = {
        "planted_status": planted.get("status"),
        "planted_coverage(sel,done,fail)": coverage(planted),
        "clean_status": clean.get("status"),
        "clean_coverage(sel,done,fail)": coverage(clean),
        "planted_completed": planted_ok,
        "clean_completed": clean_ok,
        "matches": matches,
        "planted_comment_count": len(findings),
        "clean_comment_count": len(clean_findings) if clean_findings is not None else None,
        "clean_comments_for_manual_adjudication": clean_findings or [],
        "automatic_verdict": verdict,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if meets_auto else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
