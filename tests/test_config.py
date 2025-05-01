import unittest
import os
import json
from unittest.mock import patch, mock_open, MagicMock
import config
from argparse import Namespace

class TestConfig(unittest.TestCase):

    def setUp(self):
        config._config = None
        for var in ["TEST_PARAM", "MY_VAR", "MY_DICT", "test1", "test2", "ENV_ONLY", "SAMPLE_VAR"]:
            os.environ.pop(var, None)

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"TEST_PARAM": "test_value"}')
    @patch("config.os.getcwd", return_value="/some/path")
    def test_get_parameter_from_file(self, mock_getcwd, mock_open_file, mock_isfile):
        value = config.get_parameter("TEST_PARAM")
        self.assertEqual(value, "test_value")

    def test_get_parameter_from_env(self):
        os.environ["TEST_PARAM"] = "json:true"
        value = config.get_parameter("TEST_PARAM")
        self.assertEqual(value, True)

    def test_get_parameter_with_default(self):
        value = config.get_parameter("NON_EXISTENT_PARAM", default="default_value")
        self.assertEqual(value, "default_value")

    def test_get_parameter_not_found(self):
        value = config.get_parameter("UNKNOWN_PARAM")
        self.assertIsNone(value)

    def test_convert_to_typed_value(self):
        self.assertEqual(config.convert_to_typed_value("true"), True)
        self.assertEqual(config.convert_to_typed_value("123"), 123)
        self.assertEqual(config.convert_to_typed_value("[1,2,3]"), [1,2,3])
        self.assertEqual(config.convert_to_typed_value("{\"a\":1}"), {"a": 1})
        self.assertEqual(config.convert_to_typed_value("not_json"), "not_json")
        self.assertEqual(config.convert_to_typed_value(None), None)

    def test_set_parameter_string(self):
        config.set_parameter("MY_VAR", "hello")
        self.assertEqual(os.environ["MY_VAR"], "hello")

    def test_set_parameter_object(self):
        config.set_parameter("MY_DICT", {"a": 1})
        self.assertTrue(os.environ["MY_DICT"].startswith("json:"))
        self.assertEqual(config.get_parameter("MY_DICT"), {"a": 1})

    def test_overwrite_from_args(self):
        args = Namespace(test1="value1", test2=123)
        config.overwrite_from_args(args)
        self.assertEqual(os.environ["test1"], "value1")
        self.assertEqual(json.loads(os.environ["test2"][5:]), 123)

    @patch("os.path.isfile", return_value=False)
    @patch("config.os.getcwd", return_value="/does/not/exist")
    def test_get_default_path_returns_none(self, mock_getcwd, mock_isfile):
        self.assertIsNone(config._get_default_path())

    @patch("os.path.isfile", side_effect=[False, True])
    @patch("config.os.getcwd", return_value="/a/b/c")
    def test_get_default_path_finds_file(self, mock_getcwd, mock_isfile):
        path = config._get_default_path()
        self.assertTrue(path.endswith("config.json"))

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("config._get_default_path", return_value="config.json")
    def test_init_config_loads_once(self, mock_path, mock_open_file):
        config._config = None
        config._init_config()
        config._init_config()  # Should not reload
        self.assertEqual(config._config["key"], "value")

    def test_get_parameter_prefers_env_over_config(self):
        os.environ["ENV_ONLY"] = "json:100"
        config._config = {"ENV_ONLY": 999}
        result = config.get_parameter("ENV_ONLY")
        self.assertEqual(result, 100)

    @patch("config._get_default_path", return_value=None)
    def test_init_config_empty_when_no_file(self, mock_default_path):
        config._config = None
        config._init_config()
        self.assertEqual(config._config, {})

    def test_set_and_get_env_json(self):
        config.set_parameter("SAMPLE_VAR", [1, 2, 3])
        result = config.get_parameter("SAMPLE_VAR")
        self.assertEqual(result, [1, 2, 3])

if __name__ == "__main__":
    unittest.main()