import random
import requests
import os

if 'DEBUG' in os.environ:
    API = 'https://localhost'
else:
    API = 'https://6peln83v5l.execute-api.us-east-1.amazonaws.com/dev'


def add_recipe(persistant_attributes, recipe):
    if 'recipes' in persistant_attributes:
        persistant_attributes['recipes'].append(recipe)
    else:
        persistant_attributes['recipes'] = [recipe]


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
        return recipe
    else:
        return None


def search_online_recipes(recipe_name):
    # first make a GET request to the /search endpoint
    response = requests.get(API + '/search', params={'keywords': recipe_name})
    if not response.ok:
        return []
    if response.headers['Content-Type'] != 'application/json':
        return []

    # we've got some recipes to go through now
    json = response.json()

    if json['code'] < 0:
        return []
    elif json['code'] == 1:
        return []

    recipes = json['data']

    # some rank/search algorithm goes here, but it needs to be shared code with
    # how we search cookbook. but for now we just return everything
    return recipes


def get_my_recipe(persistant_attributes, recipe_id):
    return None


def search_my_recipes(persistant_attributes, recipe_name):
    if 'recipes' not in persistant_attributes:
        return []

    recipes = persistant_attributes['recipes']

    if len(recipes) == 0:
        return []

    # some rank/search algorithm goes here, but it needs to be shared code with
    # how we search online
    # for now we just send them all
    return recipes
