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
        "status": "completed",
        "manifest": {
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


if __name__ == "__main__":
    unittest.main()
