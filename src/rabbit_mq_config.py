import json
import recipe_database


import pika

class RabbitMQConfig:
    def __init__(self, host='rabbitmq', port=5672, queue_name='search_requests'):
        self.host = host
        self.port = port
        self.queue_name = queue_name

    def get_connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        return connection

    def send_message_to_queue(self, message):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        message_json = json.dumps(message)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message_json)
        connection.close()


    def consume_messages(self):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
    
        def inner_callback(ch, method, properties, body):
            recipe_database.save_receipt_info(body.decode('utf-8'))

        channel.basic_consume(queue=self.queue_name, on_message_callback=inner_callback, auto_ack=True)
        print('Waiting for search requests. To exit, press CTRL+C')
        channel.start_consuming()

