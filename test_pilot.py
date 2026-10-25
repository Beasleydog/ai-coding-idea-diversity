"""Offline checks for the measurement, historical cutoff, evidence and spend guard."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from pilot import Pilot, bootstrap, diversity, load, redact, validate_answer


class MeasurementTests(unittest.TestCase):
    def test_fast_score_matches_all_pairs(self):
        rng = np.random.default_rng(448)
        for n in (2, 5, 20):
            x = rng.normal(size=(n, 384))
            x /= np.linalg.norm(x, axis=1, keepdims=True)
            expected = np.mean([1 - x[i] @ x[j] for i in range(n) for j in range(i + 1, n)])
            self.assertAlmostEqual(diversity(x), expected, places=12)

    def test_known_geometry_and_bad_inputs(self):
        self.assertAlmostEqual(diversity([[1, 0], [1, 0]]), 0)
        self.assertAlmostEqual(diversity([[1, 0], [0, 1]]), 1)
        self.assertAlmostEqual(diversity([[1, 0], [-1, 0]]), 2)
        for value in ([[1, 0]], [[0, 0], [1, 0]], [[float("nan"), 0], [1, 0]]):
            with self.assertRaises(ValueError):
                diversity(value)

    def test_bootstrap_is_reproducible(self):
        x = np.eye(5)
        self.assertEqual(bootstrap(x, repetitions=100), bootstrap(x, repetitions=100))


class EvidenceTests(unittest.TestCase):
    def test_hallucinated_quote_is_rejected(self):
        answer = {"label": "project", "label_quote": "Build a timer", "idea": "A timer.",
                  "idea_quotes": ["Build a timer"], "ai_topic": False}
        self.assertEqual(validate_answer(answer, "Build a timer for focused work."), answer)
        answer["idea_quotes"] = ["Invented feature"]
        with self.assertRaises(ValueError):
            validate_answer(answer, "Build a timer for focused work.")

    def test_identity_and_date_redaction(self):
        value = redact("alice/tool by alice, 2021-01-02 https://example.com", "alice/tool")
        self.assertNotIn("alice", value)
        self.assertNotIn("2021", value)
        self.assertNotIn("https://", value)

    def test_redaction_preserves_project_meaning(self):
        value = redact("Cyberpunk 2077 mod by alice: distributed charging, 2021.", "alice/charging")
        self.assertIn("Cyberpunk 2077", value)
        self.assertIn("distributed charging", value)
        self.assertNotIn("alice", value)
        self.assertIn("A camera", redact("A camera by a", "a/project"))

    def test_commit_after_cutoff_is_rejected(self):
        pilot = Pilot.__new__(Pilot)
        meta = {"fork": False, "full_name": "a/b", "name": "b", "owner": {"login": "a"},
                "created_at": "2021-01-01T00:00:00Z", "default_branch": "main"}
        commits = [{"commit": {"committer": {"date": "2021-02-01T00:00:00Z"}}, "sha": "abc"}]
        with patch.object(pilot, "github", side_effect=[meta, commits]):
            with self.assertRaisesRegex(LookupError, "commit_outside_age_window"):
                pilot.snapshot({"id": 1, "created_at": meta["created_at"]})

    def test_budget_blocks_post_before_network(self):
        pilot = Pilot.__new__(Pilot)
        pilot.budget = 0.000001
        pilot.pricing = {"input_usd_per_mtok": 0.15, "output_usd_per_mtok": 0.5}
        pilot.key = "not-a-real-key"
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            pilot.cache = Path(tmp)
            with self.assertRaisesRegex(RuntimeError, "exceed budget"):
                pilot.classify({"readme": "A simple timer for focus.", "paths": "timer.py"})

    def test_failed_post_keeps_reservation(self):
        pilot = Pilot.__new__(Pilot)
        pilot.budget = 0.003
        pilot.pricing = {"input_usd_per_mtok": 0.15, "output_usd_per_mtok": 0.5}
        pilot.key = "not-a-real-key"
        pilot.http = Mock()
        pilot.http.post.side_effect = ConnectionError("uncertain transport failure")
        payload = {"messages": [], "max_tokens": 3072}
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            pilot.cache = Path(tmp)
            with self.assertRaises(ConnectionError):
                pilot.complete(payload)
            self.assertEqual(len(load(pilot.cache / "spend.json")), 1)
            with self.assertRaisesRegex(RuntimeError, "exceed budget"):
                pilot.complete(payload)
            self.assertEqual(pilot.http.post.call_count, 1)

    def test_authenticated_private_repo_is_not_collected(self):
        pilot = Pilot.__new__(Pilot)
        with patch.object(pilot, "github", return_value={"private": True}):
            with self.assertRaisesRegex(LookupError, "currently_private"):
                pilot.snapshot({"id": 1})


if __name__ == "__main__":
    unittest.main()
