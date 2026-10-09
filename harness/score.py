"""Score an OCR JSON result against the pre-registered ground truth. Usage: score.py truth.json planted.json clean.json"""
import json, sys
truth = json.load(open(sys.argv[1], encoding="utf-8"))
def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception as e: return {"status": f"unreadable: {e}"}
def lines(c):
    out = []
    for k in ("line", "start_line", "end_line", "startLine", "endLine", "new_line"):
        v = c.get(k)
        if isinstance(v, int): out.append(v)
    loc = c.get("location") or c.get("range") or {}
    if isinstance(loc, dict):
        out += [v for v in loc.values() if isinstance(v, int)]
    return out
def comments(r): return r.get("comments") or []
def coverage(r):
    cov = (r.get("manifest") or {}).get("coverage") or {}
    return len(cov.get("selected", [])), len(cov.get("completed", [])), len(cov.get("failed", []))
P, C = load(sys.argv[2]), load(sys.argv[3])
tol = truth["line_tolerance"]
res = {"planted_status": P.get("status"), "planted_coverage(sel,done,fail)": coverage(P),
       "clean_status": C.get("status"), "clean_coverage(sel,done,fail)": coverage(C), "matches": {}}
for d in truth["planted"]:
    hit = None
    for c in comments(P):
        text = " ".join(str(c.get(k, "")) for k in ("content", "existing_code", "suggestion_code")).lower()
        s, e = c.get("start_line"), c.get("end_line")
        near = any(abs(l - d["line"]) <= tol for l in lines(c)) or (
            isinstance(s, int) and isinstance(e, int) and s <= d["line"] <= e)
        if near and any(k.lower() in text for k in d["keywords"]):
            hit = c; break
    res["matches"][d["id"]] = bool(hit)
res["planted_comment_count"] = len(comments(P))
res["clean_comment_count"] = len(comments(C))
res["clean_comments_for_manual_adjudication"] = comments(C)
auto_ok = (coverage(P)[1:] == (1, 0) and coverage(C)[1:] == (1, 0)
           and all(res["matches"].values()) and len(comments(C)) <= 1)
res["automatic_verdict"] = ("PROVISIONAL_PASS_PENDING_CLEAN_ADJUDICATION" if auto_ok and comments(C)
                            else "PASS_AUTOMATIC_CRITERIA" if auto_ok else "NOT_QUALIFIED")
print(json.dumps(res, indent=2))
