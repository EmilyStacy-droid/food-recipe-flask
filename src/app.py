#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import re
import os
from prometheus_client import Counter
import rabbit_mq_config
import recipe_utils

app = Flask(__name__, template_folder='templates')

view_metric = Counter('view_total', 'Homepage view', ['page'])


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

    total_calories = 0
    num_recipes = len(recipe_list)
    
    for recipe in recipe_list:
        calories = extract_calories(recipe['summary'])
        recipe['calories'] = calories
        total_calories += calories
    
    average_calories = total_calories / num_recipes if num_recipes > 0 else 0

    rabbit_mq_config.send_message_to_queue(recipe_list)
    return render_template('index.html', recipes=recipe_list, average_calories=average_calories)

@app.route("/health", methods=["GET"])
def get_health():
    return jsonify({"status":"OK"},200)

def extract_calories(recipe_description):
    match = re.search(r'(\d+)\s+calories', recipe_description)
    if match:
        return int(match.group(1))
    else:
        return 0

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print('Exception happen when app runs',e)