import boto3
from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

from my_cookbook.util import core
from my_cookbook.util import requester
import lambda_function

test_recipe = {
    "category": {
        "name": "breakfast",
        "subcategory": {
            "attributes": "buttermilk",
            "name": "pancakes"
        }
    },
    "cook_time": "10 minutes",
    "ingredients": [
        {
            "name": "flour"
        }, {
            "name": "salt"
        }, {
            "name": "baking soda"
        }, {
            "name": "baking powder"
        }, {
            "name": "egg"
        }, {
            "name": "buttermilk"
        }, {
            "name": "butter"
        }
    ],
    "instructions": [
        {
            "speech": [
                "mix", {
                    "name": "flour",
                    "quantity": 0.5,
                    "units": "cups"
                }, "with", {
                    "name": "salt",
                    "quantity": 0.25,
                    "units": "teaspoon"
                }, ",", {
                    "name": "baking soda",
                    "quantity": 0.25,
                    "units": "teaspoon"
                }, ", and", {
                    "name": "baking powder",
                    "quantity": 0.5,
                    "units": "teaspoon"
                }
            ]
        }, {
            "speech": [
                "beat in an", {
                    "name": "egg",
                    "quantity": 1,
                    "units": "None"
                }, "and", {
                    "name": "buttermilk",
                    "quantity": 0.5,
                    "units": "cups"
                }
            ]
        }, {
            "speech": [
                "melt the", {
                    "name": "butter",
                    "quantity": 1,
                    "units": "tablespoon"
                }, "and beat into the batter"
            ]
        }
    ],
    "main_ingredient": "buttermilk",
    "name": "classic buttermilk pancakes",
    "nutrition": {
        "fat": {
            "unit": "g",
            "value": 2
        },
        "sodium": {
            "unit": "g",
            "value": 1
        }
    },
    "prep_time": "10 minutes",
    "tags": [
        "sweet", "buttery", "warm"
    ],
    "total_time": "20 minutes"
}


def insert_recipes():
    # insert a recipe into the users cookbook
    attrs = {core.STATE_KEY: core.States.ASK_SAVE, 'current_recipe': test_recipe}
    intent = requester.Intent('AMAZON.YesIntent').build()
    req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
    ).with_attributes(attrs).build()
    return lambda_function.handle_event(req, None)


def delete_table(endpoint_url):
    """deletes the table if it already exists"""
    client = boto3.client(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")
    tables = client.list_tables()['TableNames']
    if core.DB_TABLE in tables:
        client.delete_table(TableName=core.DB_TABLE)


def wip(f):
    return attr('wip')(f)
