#!/usr/bin/env python3
import sqlite3
import requests 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'

db = SQLAlchemy(app)

'''
Define the database model
that is used to store 
the recipe Id and details.
'''
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
   

class RecipesInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("Recipes.id"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    servings = db.Column(db.Integer)
    readyInMin = db.Column(db.Integer)
    healthScore = db.Column(db.Float, default = 0.00)
    cheap = db.Column(db.Boolean, default=False)

'''
Helper function to get Id
using API
'''
load_dotenv()
api_key = os.getenv("API_KEY")

def get_recipe_id():
    requestUrl = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&number=10"
    response = requests.get(requestUrl)
    return response.json()

'''
In main first get the recipe ids and then 
create a new object that we can add to the database. 
'''

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        recipe_id_list = get_recipe_id()
        for recipe in recipe_id_list ["results"]:
            print(recipe)
            new_entry = Recipes(id=recipe["id"], title = recipe["title"])
            db.session.add(new_entry)
            db.session.commit()

