#!/usr/bin/env python3
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
db = SQLAlchemy(app)

class RecipeDatabase:

    class RecipeInfo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        recipe_id = db.Column(db.Integer, nullable=False)
        title = db.Column(db.String(50), nullable=False)
        servings = db.Column(db.Integer)
        readyInMin = db.Column(db.Integer)
        healthScore = db.Column(db.Float, default=0.00)
        cheap = db.Column(db.Boolean, default=False)

    class RequestInfo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cuisine = db.Column(db.String(50))
        calories = db.Column(db.Integer)

def save_receipt_info(recipe_list):
    for recipe in recipe_list:
        new_recipe_info = RecipeDatabase.RecipeInfo(
        recipe_id=recipe['id'],
        title=recipe['title'],
        servings=recipe['servings'],
        readyInMin=recipe['ready_in_min'],
        healthScore=recipe['health_score'],
        cheap=recipe['cheap']
            )
    db.session.add(new_recipe_info)
    db.session.commit()
     
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
