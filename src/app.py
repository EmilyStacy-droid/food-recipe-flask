#!/usr/bin/env python3
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

# @app.route("/")
# def main():
#     return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    min_calaries = int(request.form.get('min_calories', 0))
    cuisine = request.form.get('cuisine', '')
    returned_str = f"You want to have a {cuisine} cusine with min {min_calaries} calaries"
    return "You entered: " + returned_str

if __name__ == '__main__':
    app.run(debug=True)