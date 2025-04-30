import unittest
from unittest.mock import patch, mock_open, MagicMock
from collections import Counter, defaultdict
import json
from Analysis import analysisOne
import matplotlib.pyplot as plt

class TestAnalysisOne(unittest.TestCase):

    def setUp(self):
        # Sample mock issue dataset
        self.sample_data = [
            {
                "user": {"login": "user1"},
                "closed_by": {"login": "user2"},
                "reactions": {
                    "url": "https://api.github.com/repos/test/test/issues/1/reactions",
                    "+1": 5,
                    "-1": 1,
                    "laugh": 3,
                    "hooray": 2,
                    "confused": 1,
                    "heart": 4,
                    "rocket": 2,
                    "eyes": 1
                }
            },
            {
                "user": {"login": "user1"},
                "closed_by": {"login": "user3"},
                "reactions": {
                    "url": "https://api.github.com/repos/test/test/issues/2/reactions",
                    "+1": 2,
                    "heart": 1
                }
            },
            {
                "user": {"login": "user2"},
                "closed_by": None,  # No closer for this issue
                "reactions": {}  # No reactions
            },
            {
                "user": {"login": "user3"},
                "closed_by": {"login": "user2"},
                "reactions": {
                    "url": "https://api.github.com/repos/test/test/issues/4/reactions",
                    "laugh": 1
                }
            },
            {
                # Missing user information
                "closed_by": {"login": "user1"},
                "reactions": {
                    "+1": 1
                }
            }
        ]

    @patch("builtins.open", new_callable=mock_open)
    def test_load_data(self, mock_file):
        """Test that load_data correctly loads and returns JSON data."""
        # Mock the json.load to return our sample data
        with patch("json.load", return_value=self.sample_data):
            result = analysisOne.load_data("fake_path.json")
            
            # Verify the file was opened
            mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")
            
            # Verify the data was returned correctly
            self.assertEqual(result, self.sample_data)
            self.assertEqual(len(result), 5)

    def test_analyze_contributors_and_reactions(self):
        """Test that analyze_contributors_and_reactions correctly processes the data."""
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions(self.sample_data)
        
        # Test creators counting
        self.assertEqual(creators["user1"], 2)
        self.assertEqual(creators["user2"], 1)
        self.assertEqual(creators["user3"], 1)
        
        # Test closers counting
        self.assertEqual(closers["user2"], 2)
        self.assertEqual(closers["user3"], 1)
        self.assertEqual(closers["user1"], 1)
        
        # Test reaction counting
        self.assertEqual(reactions["+1"], 8)
        self.assertEqual(reactions["-1"], 1)
        self.assertEqual(reactions["laugh"], 4)
        self.assertEqual(reactions["heart"], 5)
        self.assertEqual(reactions["hooray"], 2)
        self.assertEqual(reactions["confused"], 1)
        self.assertEqual(reactions["rocket"], 2)
        self.assertEqual(reactions["eyes"], 1)
        
        # Verify that 'url' is not counted as a reaction
        self.assertNotIn("url", reactions)

    def test_analyze_contributors_and_reactions_edge_cases(self):
        """Test edge cases for analyze_contributors_and_reactions."""
        # Test with empty data
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions([])
        self.assertEqual(len(creators), 0)
        self.assertEqual(len(closers), 0)
        self.assertEqual(len(reactions), 0)
        
        # Test with malformed data (missing keys, null values)
        malformed_data = [
            {},  # Empty issue
            {"user": None},  # Null user
            {"user": {}, "closed_by": {}},  # Empty user and closed_by dicts
            {"user": {"login": "user1"}, "closed_by": "string_not_dict"},  # closed_by not a dict
            {"user": {"login": "user1"}, "reactions": None}  # Null reactions
        ]
        creators, closers, reactions = analysisOne.analyze_contributors_and_reactions(malformed_data)
        
        # Should still handle this gracefully
        self.assertEqual(creators["user1"], 1)
        self.assertEqual(len(closers), 0)
        self.assertEqual(len(reactions), 0)

    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_plot_combined(self, mock_show, mock_savefig):
        """Test that plot_combined creates the charts correctly."""
        # Create test data for the plot function
        creators = Counter({"user1": 10, "user2": 8, "user3": 6, "user4": 4})
        closers = Counter({"user2": 12, "user1": 9, "user5": 7, "user3": 5})
        reactions = {"heart": 20, "+1": 15, "laugh": 12, "-1": 8, "eyes": 5}
        
        # Call the plot function
        analysisOne.plot_combined(creators, closers, reactions, top_n=3)
        
        # Verify that the plot was saved and shown
        mock_savefig.assert_called_once_with('combined_issue_analysis.png')
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.subplots")
    def test_plot_combined_no_data(self, mock_subplots):
        """Test plot_combined with empty data."""
        # Set up mock for subplots to prevent actual plot creation
        mock_fig = MagicMock()
        mock_axes = [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Test with empty data
        with self.assertRaises(ValueError):
            # This should raise an error because zip() with empty sequences
            analysisOne.plot_combined(Counter(), Counter(), {})

    @patch("Analysis.analysisOne.load_data")
    @patch("Analysis.analysisOne.analyze_contributors_and_reactions")
    @patch("Analysis.analysisOne.plot_combined")
    @patch("builtins.print")
    def test_run(self, mock_print, mock_plot, mock_analyze, mock_load):
        """Test the main run function."""
        # Set up mocks
        mock_load.return_value = self.sample_data
        mock_analyze.return_value = (
            Counter({"user1": 2, "user2": 1, "user3": 1}),
            Counter({"user2": 2, "user3": 1, "user1": 1}),
            {"+1": 8, "heart": 5, "laugh": 4}
        )
        
        # Run the function
        analysisOne.run()
        
        # Verify the correct filepath was used
        mock_load.assert_called_once_with("data/poetry_data.json")
        
        # Verify analyze was called with the loaded data
        mock_analyze.assert_called_once_with(self.sample_data)
        
        # Verify plot was called with the analysis results
        mock_plot.assert_called_once()
        
        # Verify print was called multiple times (for each section of output)
        self.assertGreater(mock_print.call_count, 3)

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_load_data_file_not_found(self, mock_open):
        """Test error handling when the file is not found."""
        with self.assertRaises(FileNotFoundError):
            analysisOne.load_data("nonexistent_file.json")

    @patch("builtins.open", new_callable=mock_open, read_data="not valid json")
    def test_load_data_invalid_json(self, mock_file):
        """Test error handling with invalid JSON data."""
        with self.assertRaises(json.JSONDecodeError):
            analysisOne.load_data("invalid.json")

if __name__ == "__main__":
    unittest.main()