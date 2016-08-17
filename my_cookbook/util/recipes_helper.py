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
API_HEADER = {"X-BigOven-API-Key": BIGOVEN_API_KEY}


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


def search_my_recipes(recipe_name, username, password):
    return search(recipe_name, only_user=True, username=username, password=password)


def search_online_recipes(recipe_name):
    return search(recipe_name, only_user=False)


def search(recipe_name, only_user=True, username=None, password=None):
    """ searches recipes in all folders for a given user"""
    if stage.PROD:
        params = {'any_kw': recipe_name}
        if only_user and username and password:
            params['username'] = username
            response = requests.get(API + '/recipes',
                                    headers=API_HEADER,
                                    params=params,
                                    auth=requests.auth.HTTPDigestAuth(username, password))
        else:
            response = requests.get(API + '/recipes', headers=API_HEADER, params=params)

        if not response.ok:
            return []

        return response.json()
    else:
        if only_user:
            return ranker.search(recipe_name, fake_data.user_recipes)
        else:
            return ranker.search(recipe_name, fake_data.test_online_recipes)
