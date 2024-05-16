#!/usr/bin/env python3
from flask import Flask, render_template, jsonify,redirect, url_for, request
from prometheus_client import Counter
from config import rabbit_mq_config
from util import recipe_utils

app = Flask(__name__, template_folder='templates')

# Create Prometheus counters for views and purchases
view_metric = Counter('view_total', 'Homepage view', ['page'])

# Define a callback function to handle the result from RabbitMQ
rabbitmq_config = rabbit_mq_config.RabbitMQConfig()
# def consume_messages_background():
#     # Call consume_messages with handle_recipe_list as the callback function
#     while True:
#         rabbitmq_config.consume_messages(handle_recipe_list)

# def handle_recipe_list(recipe_list):
#     # Render index.html with the received recipe_list
#     return render_template('index.html', recipes=recipe_list)

@app.route("/", methods=["GET"])
def main():
    view_metric.labels("homepage").inc()
    return render_template('index.html', recipes=[])
    
@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    max_calories = int(request.form.get('max_calories', 100))
    cuisine = request.form.get('cuisine', '')
    recipe_ids = recipe_utils.get_recipe_ids({"cuisine": cuisine, "max_calories": max_calories})
    recipe_list = recipe_utils.save_recipe_details(recipe_ids)
    print("recipe_info!!!", recipe_list)
    # rabbitmq_config.send_message_to_queue({"cuisine": cuisine, "max_calories": max_calories})
    rabbitmq_config.send_message_to_queue(recipe_list)
    return render_template('index.html', recipes=recipe_list)

@app.route("/health", methods=["GET"])
def get_health():
    return jsonify({"status":"OK"},200)

if __name__ == '__main__':
    # consume_thread = Thread(target=consume_messages_background)
    # consume_thread.daemon = True
    # consume_thread.start()
    try:
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        print('Exception happen when app runs',e)