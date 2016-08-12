import logging
import random
import unittest

from my_cookbook.util import core
from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
import lambda_function

CONTEXT = {"debug": True}


class NewRecipeTest(unittest.TestCase):
    def test_recipe_in_empty_cookbook(self):
        utils.delete_table(core.LOCAL_DB_URI)

        intent = requester.Intent('StartNewRecipeIntent').with_slot(
            'RecipeName', 'Chicken and black bean burritos').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

    def test_unheard_recipe(self):
        utils.delete_table(core.LOCAL_DB_URI)

        intent = requester.Intent('StartNewRecipeIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.NEW_RECIPE)

    def test_recipe_in_cookbook(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # insert a recipe into the users cookbook
        attrs = {core.STATE_KEY: core.States.ASK_SAVE, 'current_recipe': utils.test_recipe}
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes(attrs).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)
        recipes_result = lambda_function._skill.db_helper.get('recipes')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(len(recipes_result.value), 1)

        # now ask to make that recipe
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName',
                                                                    'Pancakes').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)
