import logging
import os
import random
import requests
from recipe_ranker import ranker

from my_cookbook import stage
from my_cookbook.util import core
from my_cookbook.tests import fake_data

logging.getLogger("urllib3").setLevel(logging.WARNING)

API = 'https://api2.bigoven.com/'
BIGOVEN_API_KEY = core.load_key()
API_HEADER = {"X-BigOven-API-Key": BIGOVEN_API_KEY}

def get_online_recipe(recipe):
    recipe_id = recipe['RecipeId'] # bigoven specific
    if stage.PROD:
        response = requests.get(API + '/recipe/' + recipe_id, headers=API_HEADER)
        if not response.ok:
            return {}

        recipe = reponse.json()
        return recipe
    else:
        for online_recipe in fake_data.test_online_recipes:
            if recipe_id == online_recipe['RecipeId']:
                return online_recipe
    return {}

def search_my_recipes(recipe_name, username):
    return search(recipe_name, only_user=True, username=username)


def search_online_recipes(recipe_name):
    return search(recipe_name, only_user=False)


def search(recipe_name, only_user=True, username=None):
    """ searches recipes in all folders for a given user"""
    if stage.PROD:
        params = {'any_kw': recipe_name}

        if only_user:
            params['username'] = username

        response = requests.get(API + '/recipes', headers=API_HEADER, params=params)

        if not response.ok:
            return []

        recipes = response.json()['Results']
        return recipes
    else:
        # uses fake_data
        if only_user:
            return ranker.search(recipe_name, fake_data.user_recipes)
        else:
            return ranker.search(recipe_name, fake_data.test_online_recipes)
