import requests
import os
from dotenv import load_dotenv

'''
Helper function to get Id
using API
'''
load_dotenv()
api_key = os.getenv("API_KEY")

def get_recipe_ids(request=None):
    if request:
        cuisine = request["cuisine"]
        max_calories = request["max_calories"]
        requestUrl = f"https://api.spoonacular.com/recipes/complexSearch??cousine={cuisine}&maxCalories={max_calories}&apiKey={api_key}&number=3"
    else:
        requestUrl = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&number=1"
    
    response = requests.get(requestUrl, timeout=10)
    response_json = response.json()
    recipes = response_json.get('results', [])
    return [(recipe['id'], recipe['title']) for recipe in recipes]
    





'''
In main first get the recipe ids and then 
create a new object that we can add to the database. 
'''

def save_recipe_details(id_list):
    recipe_info_list = []
    for recipe_id, title in id_list:
        requestUrl = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false&apiKey={api_key}"
        response = requests.get(requestUrl, timeout=10)
        recipe_info = response.json()
        recipe_info_list.append({
        'id': recipe_id,
        'title': title,
        'servings': recipe_info.get('servings', None),
        'ready_in_min': recipe_info.get('readyInMinutes', None),
        'health_score': recipe_info.get('healthScore', None),
        'cheap': recipe_info.get('cheap', False),
        'summary': recipe_info.get('summary', None),
        'image_url' : recipe_info.get('image',None)
    })
    return recipe_info_list
        
   