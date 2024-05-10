#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify
from prometheus_client import Counter

app = Flask(__name__, template_folder='templates')

# Create Prometheus counters for views and purchases
view_metric = Counter('view_total', 'Homepage view', ['page'])

@app.route("/", methods=["GET"])
def main():
    view_metric.labels("homepage").inc()
    return render_template('index.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    min_calaries = int(request.form.get('min_calories', 0))
    cuisine = request.form.get('cuisine', '')
    returned_str = f"You want to have a {cuisine} cusine with min {min_calaries} calaries"
    return "You entered: " + returned_str


@app.route("/health", methods=["GET"])
def get_health():
    return jsonify({"status":"OK"},200)

if __name__ == '__main__':
    app.run(host='0.0.0.0')