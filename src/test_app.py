import unittest
from unittest.mock import patch, MagicMock
import sys
sys.modules['pika'] = MagicMock()

from app import app  # Adjust according to your actual app structure

@patch('recipe_utils.get_recipe_ids',  return_value=[123, 456])
@patch('recipe_utils.save_recipe_details', return_value=[{'summary': 'Recipe summary example'}])
@patch('rabbit_mq_config.pika.BlockingConnection')
class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_echo_input(self, mock_blocking_connection, mock_save_recipe_details, mock_get_recipe_ids):
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Simulate the POST request to your Flask endpoint
        response = self.app.post('/echo_user_input', data={'cuisine': '', 'max_calories': 100})

        # Assertions to ensure methods were called correctly
        mock_get_recipe_ids.assert_called_once_with({"cuisine": '', "max_calories": 100})
        mock_save_recipe_details.assert_called_once()
        mock_blocking_connection.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue='search_requests')
        mock_channel.basic_publish.assert_called_once()

        # Ensure the response status code is correct (assuming 200 for a successful post)
        self.assertEqual(response.status_code, 200)

    @patch('app.jsonify')
    def test_get_health(self, mock_jsonify, mock_blocking_connection, mock_save_recipe_details, mock_get_recipe_ids):
        mock_jsonify.return_value = {"status": "OK"}

        # Simulate the GET request to your Flask endpoint
        response = self.app.get('/health')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

if __name__ == '__main__':
    unittest.main()
