#!/usr/bin/env python3
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

# @app.route("/")
# def main():
#     return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        min_calaries = int(request.form.get('min_calories', 0))
        cuisine = request.form.get('cuisine', '')
        returned_str = f"You want to have a {cuisine} cusine with min {min_calaries} calaries"
        return render_template('index.html', data=returned_str)
    else:
        return render_template('index.html')
   
if __name__ == '__main__':
    app.run(debug=True)