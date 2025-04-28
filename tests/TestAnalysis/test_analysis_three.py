import unittest
from unittest.mock import patch, mock_open
from Analysis import analysisThree

class TestAnalysisThree(unittest.TestCase):

    def setUp(self):
        # Sample minimal mock issue dataset
        self.sample_issues = [
            {
                "created_at": "2024-01-01T00:00:00Z",
                "closed_at": "2024-01-05T00:00:00Z",
                "labels": [{"name": "bug"}],
                "comments": 4,
                "user": {"login": "user1"}
            },
            {
                "created_at": "2024-02-01T00:00:00Z",
                "closed_at": None,
                "labels": [{"name": "bug"}],
                "comments": 2,
                "user": {"login": "user2"}
            },
            {
                "created_at": "2024-03-01T00:00:00Z",
                "closed_at": "2024-03-03T00:00:00Z",
                "labels": [{"name": "kind/feature"}],
                "comments": 1,
                "user": {"login": "user1"}
            }
        ]

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("matplotlib.pyplot.show")  # prevent plots from blocking test run
    def test_run_with_label_bug(self, mock_show, mock_json_load, mock_file):
        """
        Test run() function with label 'bug'.
        Should process two issues correctly without error.
        """
        mock_json_load.return_value = self.sample_issues

        # Should not crash, should print insights
        analysisThree.run(label="bug")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("matplotlib.pyplot.show")
    def test_run_with_label_kind_feature(self, mock_show, mock_json_load, mock_file):
        """
        Test run() function with label 'kind/feature'.
        Should process one issue correctly without error.
        """
        mock_json_load.return_value = self.sample_issues

        analysisThree.run(label="kind/feature")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_run_with_no_label_provided(self, mock_json_load, mock_file):
        """
        Test run() function when no label is provided.
        Should print warning and exit safely.
        """
        analysisThree.run(label=None)  # Should handle safely

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    @patch("matplotlib.pyplot.show")
    def test_run_with_no_matching_label(self, mock_show, mock_json_load, mock_file):
        """
        Test run() function when a non-existent label is given.
        Should handle gracefully and print no matching issues.
        """
        mock_json_load.return_value = self.sample_issues

        analysisThree.run(label="nonexistent-label")  # Should handle safely

if __name__ == "__main__":
    unittest.main()
