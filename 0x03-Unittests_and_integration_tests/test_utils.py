#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch, Mock
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
    @parameterized.expand([
    ({}, ("a",), "a"),
    ({"a": 1}, ("a", "b"), "b"),
])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], expected_key)
        
class TestGetJson(TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")  # 👈 patch where requests.get is USED
    def test_get_json(self, test_url, test_payload, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
        
    @patch('utils.requests.get')
    def test_get_json_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        
        url = "http://example.com"
        with self.assertRaises(Exception) as cm:
            get_json(url)
        
        self.assertEqual(str(cm.exception), "Network error")

        
        
if __name__ == "__main__":
    unittest.main()
    