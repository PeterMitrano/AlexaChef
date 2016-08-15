import logging
import random
import unittest

from my_cookbook.util import core
from my_cookbook.tests import test_util
from my_cookbook.tests import fake_data
from my_cookbook.util import requester
from my_cookbook.util import responder
import lambda_function

@test_util.wip
class NoRecipesTest(unittest.TestCase):
    def test_recipe_in_empty_cookbook(self):
        test_util.delete_table(core.LOCAL_DB_URI)

        intent = requester.Intent('StartNewRecipeIntent').with_slot(
            'RecipeName', 'Chicken and black bean burritos').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

    def test_unheard_recipe(self):
        test_util.delete_table(core.LOCAL_DB_URI)

        intent = requester.Intent('StartNewRecipeIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.NEW_RECIPE)

@test_util.wip
class CookbookRecipeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_util.delete_table(core.LOCAL_DB_URI)

        # insert a recipe into the users cookbook
        attrs = {core.STATE_KEY: core.States.ASK_SAVE, 'current_recipe': fake_data.test_recipe}
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes(attrs).build()
        response_dict = lambda_function.handle_event(req, None)
        recipes_result = lambda_function._skill.db_helper.get('recipes')

    def test_recipe_not_in_cookbook(self):
        # ask to make something else
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName', 'Chicken Pot Pie').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new(
        ).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_SEARCH)

    def test_recipe_in_cookbook(self):
        # ask to make the recipe we had
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName',
                                                                    'Pancakes').build()
        req = requester.Request().new().with_type(requester.Types.INTENT).with_intent(intent).with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)

        #then test saving it
        intent = requester.Intent('SaveIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes']['tmp_state'], core.States.ASK_MAKE_COOKBOOK)
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.CONFIRM_OVERWRITE_RECIPE)

        # confirm yes to overwrite
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))

        #then make sure we can pick up where we left off
        intent = requester.Intent('AMAZON.YesIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.INGREDIENTS_OR_INSTRUCTIONS)

