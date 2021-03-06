import logging
import random
import unittest

from my_cookbook.util import core
from my_cookbook.tests import test_util
from my_cookbook.tests import fake_data
from my_cookbook.util import requester
from my_cookbook.util import responder
import lambda_function


class NoRecipesTest(unittest.TestCase):
    def test_unheard_recipe(self):
        test_util.delete_table(core.LOCAL_DB_URI)

        intent = requester.Intent('StartNewRecipeIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).new().attributes(
            {core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.NEW_RECIPE)


class CookbookRecipeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_util.delete_table(core.LOCAL_DB_URI)
        test_util.set_bigoven_username()

    def test_recipe_not_in_cookbook(self):
        # ask to make something else
        intent = requester.Intent('StartNewRecipeIntent').slot('RecipeName', 'pizza').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).attributes(
            {core.STATE_KEY: core.States.INITIAL_STATE}).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

        # agree to search online
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).copy_attributes(
            response_dict).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_ONLINE)

        # agree to make the one recipe it found
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).copy_attributes(
            response_dict).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)

        # ask to go right to instructions
        intent = requester.Intent('InstructionsIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).copy_attributes(
            response_dict).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))

    def test_unique_recipe_in_cookbook(self):
        # ask to make the recipe we have one of
        intent = requester.Intent('StartNewRecipeIntent').slot('RecipeName', 'Pancakes').build()
        req = requester.Request().new().type(requester.Types.INTENT).intent(intent).attributes(
            {core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)

        #agree to make it
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).copy_attributes(
            response_dict).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)

        intent = requester.Intent('IngredientsIntent').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).copy_attributes(
            response_dict).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
