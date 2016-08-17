import logging
import os
import random
import requests
from recipe_ranker import ranker

from my_cookbook import stage
from my_cookbook.util import core
from my_cookbook.tests import fake_data

API = 'https://ap2.bigoven.com/'
BIGOVEN_API_KEY = core.load_key()


def favorite_recipe(recipe):
    """ favorites are just a folder """
    raise NotImplementedError("untested")


def get_recipe_by_id(recipe_id):
    raise NotImplementedError("untested")
    if stage.PROD:
        response = requests.get(API + '/recipe/' + recipe_id)

        if not response.ok:
            return None

        # we've probably got a valid response at this point
        json = response.json()
        return json
    else:
        # fake it till ya make it (to production)
        if recipe_id in fake_data.test_online_recipes:
            return fake_data.test_online_recipes[recipe_id]
        else:
            return None


def search_my_recipes(recipe_name):
    if stage.PROD:
        response = requests.get(API + '/recipes',
                                headers=headers,
                                params={'any_kw': recipe_name},
                                auth=HTTPDigestAuth(username, password))
    else:
        return ranker.search(recipe_name, fake_data.user_recipes)


def search_online_recipes(recipe_name):
    """ returns a list of recipe dicts """
    if stage.PROD:
        # first make a GET request to the /search endpoint
        header = {"X-BigOven-API-Key": BIGOVEN_API_KEY}
        response = requests.get(API + '/recipes', headers=headers, params={'any_kw': recipe_name})
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
    else:
        # fake it
        recipes = fake_data.test_online_recipes

    return ranker.search(recipe_name, recipes)
