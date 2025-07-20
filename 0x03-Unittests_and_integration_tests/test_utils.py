#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch, Mock
from utils import get_json
from utils import memoize

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
        
class TestGetJson(unittest.TestCase):
    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response
        
        url = "http://example.com"
        result = get_json(url)
        
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, {"key": "value"})
        
    @patch('utils.requests.get')
    def test_get_json_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        
        url = "http://example.com"
        with self.assertRaises(Exception) as cm:
            get_json(url)
        
        self.assertEqual(str(cm.exception), "Network error")
        
class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


        
        
if __name__ == "__main__":
    unittest.main()
    