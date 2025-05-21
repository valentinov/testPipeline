import unittest
from unittest.mock import patch

import requests
from logic.website_fetcher import WebsiteFetcher

class TestWebsiteFetcher(unittest.TestCase):

    @patch('logic.website_fetcher.requests.get')
    def test_fetch_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><body>Success</body></html>"

        fetcher = WebsiteFetcher("https://example.com")
        content = fetcher.fetch()

        self.assertEqual(content, "<html><body>Success</body></html>")
        self.assertEqual(fetcher.get_content(), content)
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch('logic.website_fetcher.requests.get')
    def test_fetch_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection error")

        fetcher = WebsiteFetcher("https://invalid.url")
        with self.assertRaises(requests.RequestException):
            fetcher.fetch()

        self.assertEqual(fetcher.get_content(), "")  # content should remain empty

if __name__ == '__main__':
    unittest.main()
