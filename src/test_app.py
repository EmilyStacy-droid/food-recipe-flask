import unittest
from unittest.mock import patch
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.jsonify')
    def test_get_health(self, mock_jsonify):
        with self.app as client:
            mock_jsonify.return_value = {"status": "OK"}
            response = client.get('/health')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "OK"})


    @patch('util.recipe_utils.get_recipe_ids')
    @patch('util.recipe_utils.save_recipe_details')
    @patch('config.rabbit_mq_config.RabbitMQConfig.send_message_to_queue')
    def test_echo_input(self, mock_send_message, mock_save_recipe_details, mock_get_recipe_ids):
        self.app.post('/echo_user_input')
        mock_get_recipe_ids.assert_called_once_with({"cuisine": '', "max_calories": 100})
        mock_save_recipe_details.assert_called_once()
        mock_send_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()