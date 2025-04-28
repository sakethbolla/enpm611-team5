import unittest
from unittest.mock import patch, mock_open, MagicMock
import os

# ✅ FIRST: Set a fake GitHub token
os.environ["GITHUB_TOKEN"] = "fake_token_for_testing"

# ✅ THEN: Patch 'open' and 'json.load' BEFORE importing fetch_issues
with patch('builtins.open', new_callable=mock_open, read_data='{}'), \
        patch('json.load', return_value={"OWNER": "dummy-owner", "REPO": "dummy-repo"}):
    import scripts.fetch_issues as fetch_issues_module


class TestFetchIssues(unittest.TestCase):

    @patch('scripts.fetch_issues.requests.get')
    def test_fetch_issues_success(self, mock_get):
        """
        Test fetching issues successfully from GitHub API.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{"id": 1, "title": "Test Issue"}],  # First page has data
            []  # Second page is empty, so it stops
        ]
        mock_get.return_value = mock_response

        issues = fetch_issues_module.fetch_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["title"], "Test Issue")

    @patch('scripts.fetch_issues.requests.get')
    def test_fetch_issue_events_success(self, mock_get):
        """
        Test fetching events for a single issue.
        """
        issue = {"events_url": "https://api.github.com/events"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{"event": "labeled"}],  # Page 1
            []  # No more data
        ]
        mock_get.return_value = mock_response

        events = fetch_issues_module.fetch_issue_events(issue)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "labeled")

    def test_save_issues_to_json(self):
        """
        Test saving issues to JSON file.
        """
        sample_issues = [{"id": 1, "title": "Test Issue"}]
        with patch("builtins.open", mock_open()) as mocked_file:
            fetch_issues_module.save_issues_to_json(sample_issues, "data/test_output.json")

        # Check file was attempted to be opened
        mocked_file.assert_called_with("data/test_output.json", "w", encoding="utf-8")

    @patch('scripts.fetch_issues.requests.get')
    def test_add_events_to_issues(self, mock_get):
        """
        Test adding events to issues list.
        """
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{"event": "assigned"}],  # First page
            []  # End
        ]
        mock_get.return_value = mock_response

        issues = [{"number": 123, "events_url": "https://api.github.com/events"}]
        updated_issues = fetch_issues_module.add_events_to_issues(issues)

        self.assertIn("events", updated_issues[0])
        self.assertEqual(updated_issues[0]["events"][0]["event"], "assigned")

    @patch('scripts.fetch_issues.requests.get')
    def test_fetch_issues_api_failure(self, mock_get):
        """
        Test fetch_issues() behavior when API call fails (non-200 response).
        """
        mock_response = MagicMock()
        mock_response.status_code = 500  # simulate failure
        mock_get.return_value = mock_response

        issues = fetch_issues_module.fetch_issues()
        self.assertEqual(issues, [])

    @patch('scripts.fetch_issues.requests.get')
    def test_fetch_issue_events_api_failure(self, mock_get):
        """
        Test fetch_issue_events() when event API fails.
        """
        issue = {"events_url": "https://api.github.com/events"}

        mock_response = MagicMock()
        mock_response.status_code = 500  # simulate failure
        mock_get.return_value = mock_response

        events = fetch_issues_module.fetch_issue_events(issue)
        self.assertEqual(events, [])

    def test_fetch_issue_events_no_events_url(self):
        """
        Test fetch_issue_events() when no events_url present.
        """
        issue = {}  # No events_url
        events = fetch_issues_module.fetch_issue_events(issue)
        self.assertEqual(events, [])

if __name__ == "__main__":
    unittest.main()
