"""Offline checks for reproducible, unfiltered monthly ID collection."""

import csv
import gzip
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import collect


class CollectionTests(unittest.TestCase):
    def test_archive_uses_unpadded_hour_and_only_creation_events(self):
        events = [
            {"type": "CreateEvent", "payload": {"ref_type": "repository"},
             "repo": {"id": 42, "name": "owner/project"}, "created_at": "2021-01-16T06:10:00Z"},
            {"type": "CreateEvent", "payload": {"ref_type": "branch"}},
            {"type": "PushEvent"},
        ]
        response = Mock()
        response.content = gzip.compress("\n".join(map(json.dumps, events)).encode())
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        with patch.object(collect.requests, "get", return_value=response) as get:
            _, events, creations, rows = collect.archive_hour("2021-01-16-06")
        self.assertEqual(get.call_args.args[0], "https://data.gharchive.org/2021-01-16-6.json.gz")
        self.assertEqual((events, creations, len(rows)), (3, 1, 1))

    def test_missing_archive_is_distinct_from_zero_events(self):
        response = Mock(status_code=404)
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        with patch.object(collect.requests, "get", return_value=response):
            self.assertEqual(collect.archive_hour("2021-01-16-06"), ("2021-01-16-06", None, None, []))

    def test_sampling_is_reproducible_and_in_month(self):
        for month in collect.MONTHS:
            self.assertEqual(collect.sample_hours(month), collect.sample_hours(month))
            self.assertTrue(collect.sample_hours(month)[0].startswith(month))
        for month in ["2021-01", "2024-02", "2025-12"]:
            windows = list(collect.minute_windows(month))
            self.assertEqual(windows[:3], list(collect.minute_windows(month))[:3])
            self.assertEqual(len(windows), len(set(windows)))
            self.assertTrue(all(x.strftime("%Y-%m") == month for x in windows))

    def test_export_ignores_old_filter_decisions(self):
        with tempfile.TemporaryDirectory(dir=collect.ROOT) as directory, patch.object(collect, "DATA", Path(directory)):
            db = collect.connect()
            for rid, status in enumerate(["excluded", "unavailable", "kept", "error", "pending"], 1):
                db.execute("INSERT INTO repos(id,name,month,rank,status) VALUES (?,?,?,?,?)", (rid, f"owner/{rid}", "2021-01", str(rid), status))
            db.commit()
            collect.export(db, 4)
            with (Path(directory) / "repositories.csv").open() as file:
                rows = list(csv.DictReader(file))
            self.assertEqual([row["id"] for row in rows], ["1", "2", "3", "4"])
            db.close()

    def test_search_rejects_incomplete_response(self):
        response = Mock()
        response.json.return_value = {"incomplete_results": True}
        start = next(collect.minute_windows("2025-11"))
        with patch.object(collect.requests, "get", return_value=response), self.assertRaises(collect.StopRun):
            collect.search_window(start, start + collect.timedelta(seconds=59), "test")

    def test_search_rejects_wrong_creation_window(self):
        response = Mock()
        response.json.return_value = {"total_count": 1, "items": [{"id": 1, "full_name": "a/b", "created_at": "2020-01-01T00:00:00Z"}]}
        start = next(collect.minute_windows("2025-11"))
        with patch.object(collect.requests, "get", return_value=response), self.assertRaises(collect.StopRun):
            collect.search_window(start, start + collect.timedelta(seconds=59), "test")


if __name__ == "__main__":
    unittest.main()
