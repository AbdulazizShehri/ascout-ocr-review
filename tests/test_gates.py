"""Offline regression tests. No API key, model, or paid service is used."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = "a" * 40
HEAD = "b" * 40

spec = importlib.util.spec_from_file_location("check_review", ROOT / "harness" / "check-review.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def result(comments=None):
    return {
        "status": "complete",
        "manifest": {
            "terminal_state": "complete",
            "input": {"exact_range": f"{BASE}..{HEAD}"},
            "coverage": {"selected": ["x"], "completed": ["x"], "failed": []},
        },
        "summary": {"budget_exceeded": False, "total_tokens": 1234},
        "warnings": [],
        "comments": [] if comments is None else comments,
    }


class QualificationTests(unittest.TestCase):
    TRUTH = {
        "line_tolerance": 3,
        "planted": [
            {"id": "P1", "line": 11, "keywords": ["traversal"]},
            {"id": "P2", "line": 20, "keywords": ["off-by-one"]},
            {"id": "P3", "line": 28, "keywords": ["injection"]},
        ],
    }
    FINDINGS = [
        {"line": 11, "content": "path traversal"},
        {"line": 20, "content": "off-by-one"},
        {"line": 28, "content": "command injection"},
    ]

    def score(self, planted=None, clean=None):
        planted = result(self.FINDINGS) if planted is None else planted
        clean = result() if clean is None else clean
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in (("truth", self.TRUTH), ("planted", planted), ("clean", clean)):
                (root / (name + ".json")).write_text(json.dumps(value), encoding="utf-8")
            p = subprocess.run(
                [sys.executable, str(ROOT / "harness" / "score.py"),
                 str(root / "truth.json"), str(root / "planted.json"), str(root / "clean.json")],
                text=True, capture_output=True, check=False,
            )
        return p.returncode, json.loads(p.stdout)

    def test_good_planted_and_clean_is_qualified(self):
        code, output = self.score()
        self.assertEqual(code, 0)
        self.assertEqual(output["automatic_verdict"], "PASS_AUTOMATIC_CRITERIA")

    def test_missing_planted_bug_fails(self):
        code, output = self.score(planted=result(self.FINDINGS[:2]))
        self.assertNotEqual(code, 0)
        self.assertFalse(output["matches"]["P3"])

    def test_one_clean_comment_requires_adjudication_and_fails_closed(self):
        code, output = self.score(clean=result([{"line": 1, "content": "potential issue"}]))
        self.assertNotEqual(code, 0)
        self.assertEqual(output["automatic_verdict"], "PROVISIONAL_PASS_PENDING_CLEAN_ADJUDICATION")

    def test_missing_coverage_fails(self):
        planted = result(self.FINDINGS)
        planted["manifest"]["coverage"]["completed"] = []
        code, output = self.score(planted=planted)
        self.assertNotEqual(code, 0)
        self.assertFalse(output["planted_completed"])

    def test_budget_exceeded_fails(self):
        planted = result(self.FINDINGS)
        planted["summary"]["budget_exceeded"] = True
        code, _ = self.score(planted=planted)
        self.assertNotEqual(code, 0)

    def test_budget_stop_warning_fails_even_if_summary_looks_clean(self):
        planted = result(self.FINDINGS)
        planted["warnings"] = [{"type": "token_budget_reached"}]
        code, _ = self.score(planted=planted)
        self.assertNotEqual(code, 0)

    def test_failed_status_fails(self):
        planted = result(self.FINDINGS)
        planted["status"] = "failed"
        code, _ = self.score(planted=planted)
        self.assertNotEqual(code, 0)


class ReviewTests(unittest.TestCase):
    def test_exact_completed_review_passes(self):
        self.assertEqual(checker.check(result(), BASE, HEAD), [])

    def test_incomplete_review_fails(self):
        value = result()
        value["manifest"]["coverage"]["completed"] = []
        self.assertTrue(checker.check(value, BASE, HEAD))

    def test_wrong_head_fails(self):
        self.assertTrue(checker.check(result(), BASE, "c" * 40))

    def test_budget_stop_fails(self):
        value = result()
        value["warnings"] = [{"type": "token_budget_reached"}]
        self.assertTrue(checker.check(value, BASE, HEAD))

    def test_no_manifest_fails(self):
        value = result()
        del value["manifest"]
        self.assertTrue(checker.check(value, BASE, HEAD))


score_spec = importlib.util.spec_from_file_location("score", ROOT / "harness" / "score.py")
scorer = importlib.util.module_from_spec(score_spec)
score_spec.loader.exec_module(scorer)
DATA = ROOT / "tests" / "data"
# Real OCR v1.12.13 outputs from run 37969387764 (qwen3:4b, NOT_QUALIFIED).
REAL_CLEAN = DATA / "real-ocr-1.12.13-clean-control-qwen3-4b.json"
REAL_PLANTED = DATA / "real-ocr-1.12.13-planted-timeout-qwen3-4b.json"


class RealOcrContractTests(unittest.TestCase):
    def load(self, path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    def test_real_successful_run_counts_as_complete(self):
        clean = self.load(REAL_CLEAN)
        self.assertEqual((clean["status"], clean["manifest"]["terminal_state"]), ("complete", "complete"))
        self.assertTrue(scorer.complete(clean))
        inp = clean["manifest"]["input"]
        self.assertEqual(checker.check(clean, inp["resolved_base"], inp["resolved_head"]), [])

    def test_real_failed_run_is_incomplete(self):
        planted = self.load(REAL_PLANTED)
        self.assertEqual(planted["status"], "failed")
        self.assertFalse(scorer.complete(planted))

    def test_real_artifacts_still_score_not_qualified(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "harness" / "score.py"), str(ROOT / "harness" / "ground-truth.json"),
             str(REAL_PLANTED), str(REAL_CLEAN)],
            capture_output=True, text=True, check=False,
        )
        output = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 1)
        self.assertTrue(output["clean_completed"])
        self.assertFalse(output["planted_completed"])
        self.assertEqual(output["automatic_verdict"], "NOT_QUALIFIED")

    def test_noncomplete_status_vocabulary_is_rejected(self):
        for status, terminal in [("completed", "complete"), ("complete", "partial"),
                                 ("partial", "partial"), ("skipped", "skipped"), ("complete", None)]:
            value = result()
            value["status"] = status
            if terminal is None:
                del value["manifest"]["terminal_state"]
            else:
                value["manifest"]["terminal_state"] = terminal
            self.assertFalse(scorer.complete(value), (status, terminal))
            self.assertTrue(checker.check(value, BASE, HEAD), (status, terminal))


if __name__ == "__main__":
    unittest.main()
