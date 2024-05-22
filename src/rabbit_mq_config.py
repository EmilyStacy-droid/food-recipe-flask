import os
import signal
import sys
import json
import pika
import recipe_database

# Function to handle termination signals
def signal_handler(signal, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

queue_name = 'search_requests' # Define the queue name

def send_message_to_queue(message):
    # Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # Start a channel
    # Declare the queue
    channel.queue_declare(queue=queue_name)
    message_json = json.dumps(message)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message_json)
    print(f" [x] Sent {message_json}")

def consume_messages():
    url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # Start a channel
    channel.queue_declare(queue=queue_name)  # Declare the queue

    def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        print(f" [x] Received {message}")
        recipe_database.save_receipt_info(message)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages:')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Gracefully shutting down...")
        connection.close()  # Close the connection to free resources
