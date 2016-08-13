import logging
import os
import random
import requests

from my_cookbook.util import core
from my_cookbook.tests import fake_data

API = 'https://6peln83v5l.execute-api.us-east-1.amazonaws.com/dev'


def add_recipe(persistant_attributes, recipe):
    if 'recipes' in persistant_attributes:
        persistant_attributes['recipes'].append(recipe)
    else:
        persistant_attributes['recipes'] = [recipe]


def get_my_recipe(persistant_attributes, recipe_id):
    if 'recipes' in persistant_attributes:
        if recipe_id in persistant_attributes['recipe']:
            return persistant_attributes['recipes'][recipe_id]

    # recipe doesn't exist
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


def get_online_recipe(recipe_id):
    if 'DEBUG' in os.environ:
        # fake it till ya make it (to production)
        if recipe_id in fake_data.test_online_recipes:
            return fake_data.test_online_recipes[recipe_id]
        else:
            return None
    else:
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
            recipe = json['data']
            return recipe
        else:
            return None


def search_online_recipes(recipe_name):
    """ returns a list of recipe dicts """
    if 'DEBUG' in os.environ:
        # fake it
        return fake_data.test_online_recipes
    else:
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
