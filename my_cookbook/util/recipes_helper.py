import random
import requests

API = 'https://6peln83v5l.execute-api.us-east-1.amazonaws.com/dev'


def get_online_recipe(recipe_id):
    response = requests.get(API + '/recipes', params={"id": recipe_id})
    if not response.ok:
        return None
    if response.headers['Content-Type'] != 'application/json':
        return None

    # we've probably got a valid response at this point
    json = response.json()

    if json['code'] < 0:
        # error
        return None
    elif json['code'] == 1:
        # wrong id
        return None
    elif json['code'] == 0:
        # found a recipe!
        recipe = json['data']
        return None


def search_online_recipes(recipe_name):
    # some rank/search algorithm goes here, but it needs to be shared code with
    # how we search online
    return []


def get_my_recipe(persistant_attributes, recipe_id):
    return None


def search_my_recipes(persistant_attributes, recipe_name):
    if 'recipes' not in persistant_attributes:
        return []

    recipes = persistant_attributes['recipes']
    # some rank/search algorithm goes here, but it needs to be shared code with
    # how we search online
    # for now we just pick a random number of them

    num_recipes = len(recipes)
    fake_num_recipes = random.randint(0, num_recipes)
    relavent_recipes = []
    for i in range(fake_num_recipes):
        relavent_recipes.append(recipes[random.randint(0, num_recipes)])

    return relavent_recipes
