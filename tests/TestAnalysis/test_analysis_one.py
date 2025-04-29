import unittest
from unittest.mock import patch, mock_open
from collections import Counter, defaultdict
import builtins

# Import after patching
from Analysis import analysisOne

class TestAnalysisOne(unittest.TestCase):

    def setUp(self):
        # Minimal sample issues
        self.sample_issues = [
            {
                "user": {"login": "user1"},
                "closed_by": {"login": "closer1"},
                "reactions": {"+1": 3, "-1": 1, "laugh": 2}
            },
            {
                "user": {"login": "user2"},
                "closed_by": {"login": "closer2"},
                "reactions": {"+1": 2, "hooray": 1}
            },
            {
                "user": {"login": "user1"},
                "closed_by": None,  # No closer
                "reactions": {"-1": 1}
            }
        ]

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_data(self, mock_json_load, mock_file):
        """
        Test loading data from a file.
        """
        mock_json_load.return_value = self.sample_issues
        result = analysisOne.load_data("dummy_path.json")
        self.assertEqual(result, self.sample_issues)

    def test_analyze_contributors_and_reactions(self):
        """
        Test contributor counting and reaction counting.
        """
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions(self.sample_issues)

        # Check creators
        expected_creators = Counter({"user1": 2, "user2": 1})
        self.assertEqual(creators, expected_creators)

        # Check closers
        expected_closers = Counter({"closer1": 1, "closer2": 1})
        self.assertEqual(closers, expected_closers)

        # Check reactions
        expected_reactions = defaultdict(int, {"+1": 5, "-1": 2, "laugh": 2, "hooray": 1})
        self.assertEqual(dict(reactions), dict(expected_reactions))

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_plot_combined(self, mock_savefig, mock_show):
        """
        Test plot_combined() doesn't crash.
        """
        creators = Counter({"user1": 5, "user2": 3})
        closers = Counter({"closer1": 4, "closer2": 2})
        reactions = {"+1": 7, "hooray": 2}

        try:
            analysisOne.plot_combined(creators, closers, reactions, top_n=2)
        except Exception as e:
            self.fail(f"plot_combined raised an exception: {e}")

    @patch("analysisOne.load_data")
    @patch("analysisOne.plot_combined")
    def test_run(self, mock_plot_combined, mock_load_data):
        """
        Test run() function integration: loading, analyzing, printing, plotting.
        """
        mock_load_data.return_value = self.sample_issues

        try:
            analysisOne.run()
        except Exception as e:
            self.fail(f"run() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
