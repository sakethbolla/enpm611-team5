import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from collections import defaultdict
from analysis import frequentLabelAndResolutionTimeAnalysis
from datetime import datetime
import pandas as pd
import gzip

class TestfrequentLabelAndResolutionTimeAnalysis(unittest.TestCase):

    def setUp(self):
        self.sample_issues = [
            {
                "created_at": "2024-01-01T00:00:00Z",
                "closed_at": "2024-01-05T00:00:00Z",
                "labels": [{"name": "bug"}]
            },
            {
                "created_at": "2024-01-10T00:00:00Z",
                "closed_at": "2024-01-15T00:00:00Z",
                "labels": [{"name": "enhancement"}]
            },
            {
                "created_at": "2024-01-20T00:00:00Z",
                "closed_at": None,
                "labels": [{"name": "bug"}]
            }
        ]

    def test_parse_date_valid_and_invalid(self):
        valid = frequentLabelAndResolutionTimeAnalysis.parse_date("2024-01-01T00:00:00Z")
        invalid = frequentLabelAndResolutionTimeAnalysis.parse_date(None)
        malformed = frequentLabelAndResolutionTimeAnalysis.parse_date("bad-date")
        self.assertIsInstance(valid, datetime)
        self.assertIsNone(invalid)
        self.assertIsNone(malformed)

    @patch("gzip.open")
    @patch("json.load")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_run_executes_plot_and_dataframe(self, mock_show, mock_savefig, mock_json_load, mock_gzip):
        mock_json_load.return_value = self.sample_issues

        with patch("builtins.print") as mock_print:
            frequentLabelAndResolutionTimeAnalysis.run(top_n=2)

            mock_savefig.assert_called_once()
            mock_show.assert_called_once()
            self.assertTrue(mock_print.called)

    def test_dataframe_generation_logic(self):
        # Recreate label collection and aggregation manually
        label_counts = defaultdict(int)
        label_res_times = defaultdict(list)

        for issue in self.sample_issues:
            created = frequentLabelAndResolutionTimeAnalysis.parse_date(issue.get("created_at"))
            closed = frequentLabelAndResolutionTimeAnalysis.parse_date(issue.get("closed_at"))
            label_names = [lbl.get("name") for lbl in issue.get("labels", []) if lbl.get("name")]

            for lbl in label_names:
                label_counts[lbl] += 1
                if created and closed:
                    days = (closed - created).total_seconds() / 86400
                    label_res_times[lbl].append(days)

        df = pd.DataFrame({
            "label": list(label_counts.keys()),
            "issue_count": list(label_counts.values()),
            "avg_res_days": [
                (sum(label_res_times[lbl]) / len(label_res_times[lbl])) if label_res_times[lbl] else None
                for lbl in label_counts
            ]
        })

        self.assertIn("bug", df["label"].values)
        self.assertIn("enhancement", df["label"].values)
        self.assertEqual(df.loc[df["label"] == "bug", "issue_count"].values[0], 2)

if __name__ == "__main__":
    unittest.main()
