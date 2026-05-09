import unittest
from unittest.mock import patch
import requests
from src.llm import OllamaProvider

class TestOllamaProvider(unittest.TestCase):
    @patch('requests.post')
    def test_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError()
        provider = OllamaProvider()
        response = provider.generate_response("hi")
        self.assertIn("Could not reach Ollama", response)
        self.assertIn("ollama serve", response)

    @patch('requests.post')
    def test_timeout_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        provider = OllamaProvider()
        response = provider.generate_response("hi")
        self.assertIn("Timeout Error", response)

if __name__ == "__main__":
    unittest.main()
