import unittest
from unittest.mock import patch
from collections import Counter
from analysis import analysisOne

class TestAnalysisOne(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {
                "user": {"login": "user1"},
                "closed_by": {"login": "user2"},
                "reactions": {"+1": 5, "heart": 2, "url": "ignore"}
            },
            {
                "user": {"login": "user2"},
                "closed_by": {"login": "user3"},
                "reactions": {"+1": 3}
            }
        ]

    def test_analyze_contributors_and_reactions(self):
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions(self.sample_data)
        self.assertEqual(creators["user1"], 1)
        self.assertEqual(creators["user2"], 1)
        self.assertEqual(closers["user2"], 1)
        self.assertEqual(closers["user3"], 1)
        self.assertEqual(reactions["+1"], 8)
        self.assertEqual(reactions["heart"], 2)
        self.assertNotIn("url", reactions)

    def test_analyze_contributors_and_reactions_empty(self):
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions([])
        self.assertEqual(len(creators), 0)
        self.assertEqual(len(closers), 0)
        self.assertEqual(len(reactions), 0)

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_combined(self, mock_show, mock_savefig):
        creators = Counter({"user1": 2, "user2": 1})
        closers = Counter({"user2": 3, "user3": 1})
        reactions = {"+1": 5, "heart": 2}
        analysisOne.plot_combined(creators, closers, reactions, top_n=2)
        mock_savefig.assert_called_once_with("combined_issue_analysis.png")
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_combined_with_empty_data(self, mock_show, mock_savefig):
        creators = Counter()
        closers = Counter()
        reactions = {}
        try:
            analysisOne.plot_combined(creators, closers, reactions, top_n=2)
        except ValueError:
            self.fail("plot_combined() raised ValueError unexpectedly!")
        mock_savefig.assert_not_called()
        mock_show.assert_not_called()

    @patch("gzip.open")
    @patch("json.load")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_run_full_execution(self, mock_show, mock_savefig, mock_json_load, mock_gzip_open):
        mock_json_load.return_value = self.sample_data
        analysisOne.run()
        mock_savefig.assert_called_once()
        mock_show.assert_called_once()

if __name__ == "__main__":
    unittest.main()
