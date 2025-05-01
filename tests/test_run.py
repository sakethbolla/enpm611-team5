import unittest
from unittest.mock import patch, MagicMock
import run
import sys

class TestRunScript(unittest.TestCase):

    @patch("run.labelBasedDeepDiveAnalysis.run")
    @patch("run.config.overwrite_from_args")
    @patch("run.parse_args")
    def test_feature_3_label_based_analysis(self, mock_parse_args, mock_overwrite, mock_run):
        mock_args = MagicMock()
        mock_args.feature = 3
        mock_args.label = "bug"
        mock_parse_args.return_value = mock_args

        run.main()

        mock_run.assert_called_once_with(label="bug")
        mock_overwrite.assert_called_once_with(mock_args)

    @patch("run.contributorAndReactionAnalysis.run")
    @patch("run.config.overwrite_from_args")
    @patch("run.parse_args")
    def test_feature_1_contributor_analysis(self, mock_parse_args, mock_overwrite, mock_run):
        mock_args = MagicMock()
        mock_args.feature = 1
        mock_args.label = None
        mock_args.user = None
        mock_parse_args.return_value = mock_args

        run.main()

        mock_run.assert_called_once()
        mock_overwrite.assert_called_once_with(mock_args)

    @patch("run.frequentLabelAndResolutionTimeAnalysis.run")
    @patch("run.config.overwrite_from_args")
    @patch("run.parse_args")
    def test_feature_2_label_resolution(self, mock_parse_args, mock_overwrite, mock_run):
        mock_args = MagicMock()
        mock_args.feature = 2
        mock_args.label = None
        mock_args.user = None
        mock_parse_args.return_value = mock_args

        run.main()

        mock_run.assert_called_once()
        mock_overwrite.assert_called_once_with(mock_args)

    @patch("builtins.print")
    @patch("run.config.overwrite_from_args")
    @patch("run.parse_args")
    def test_invalid_feature(self, mock_parse_args, mock_overwrite, mock_print):
        mock_args = MagicMock()
        mock_args.feature = 0
        mock_args.label = None
        mock_args.user = None
        mock_parse_args.return_value = mock_args

        run.main()

        mock_print.assert_called_with("Need to specify which feature to run with --feature flag.")

    def test_parse_args_parser_setup_real_args(self):
        from run import parse_args
        original_argv = sys.argv
        sys.argv = ["run.py", "--feature", "2", "--user", "testuser", "--label", "bug"]
        args = parse_args()
        sys.argv = original_argv

        self.assertEqual(args.feature, 2)
        self.assertEqual(args.user, "testuser")
        self.assertEqual(args.label, "bug")

if __name__ == "__main__":
    unittest.main()
