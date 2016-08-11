import logging
import unittest

from my_cookbook.util import core
from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook import lambda_function

CONTEXT = {"debug": True}

class NewRecipeTest(unittest.TestCase):
    @utils.wip
    def test_recipe_in_empty_cookbook(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # lauch as new user, check out session attributes are in ASK_TUTORIAL
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName', 'Chicken and black bean burritos').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

    @utils.wip
    def test_unheard_recipe(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # lauch as new user, check out session attributes are in ASK_TUTORIAL
        intent = requester.Intent('StartNewRecipeIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().with_attributes({core.STATE_KEY: core.States.INITIAL_STATE}).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.NEW_RECIPE)
