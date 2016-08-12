import logging
import unittest

from my_cookbook.util import core
from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook import lambda_function

CONTEXT = {"debug": True}


class ConversationTest(unittest.TestCase):
    def test_first_time(self):
        utils.delete_table(core.LOCAL_DB_URI)

        event = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)

        # first launch on new user should result in a table entry with state set
        # as well as session attributes set correctly
        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_TUTORIAL)

        # since it was an ask, we expect sessionAttributes of response to be ASK_TUTORIAL
        # but we have no need to save to database, so state there should still be INITIAL_STATE
        state_result = lambda_function._skill.db_helper.getState()
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

    def test_returning_user(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # first launch on new user should result in a table entry with state set
        # as well as session attributes set correctly
        event = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        inv_result = lambda_function._skill.db_helper.get('invocations')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 1)

        # end the session and make sure database state is good
        event = requester.Request().with_type(requester.Types.END).copy_attributes(
            response_dict).build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        inv_result = lambda_function._skill.db_helper.get('invocations')
        state_result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 1)
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

        # on the next request we expect the have the right state
        # last response was a tell, so we don't need to call copy_attributes
        r = requester.Request()
        event = r.with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        inv_result = lambda_function._skill.db_helper.get('invocations')
        state_result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 2)
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

    def test_tutorial_conversation(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # lauch as new user, check out session attributes are in ASK_TUTORIAL
        req = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_TUTORIAL)

        # response with "Yes" to to tutorial, check that we saved state in db
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(
            requester.Intent("AMAZON_YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)
        state_result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)

        # delete user so we are prompted again, this time respond no.
        utils.delete_table(core.LOCAL_DB_URI)

        # lauch as new user again
        req = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        # response with "No" to to tutorial, check that we saved state in db
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(
            requester.Intent("AMAZON_NoIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.PROMPT_FOR_START)

    def test_recipe_conversation(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # insert recipes
        response_dict = utils.insert_recipes()
        recipes_result = lambda_function._skill.db_helper.get('recipes')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(len(recipes_result.value), 1)

        # lauch as new user, check out session attributes afterwards
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName',
                                                                    'Pancakes').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().build(
        )
        response_dict = lambda_function.handle_event(req, CONTEXT)
        recipes_result = lambda_function._skill.db_helper.get('recipes')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(len(recipes_result.value), 1)
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)

        # response with "Yes" to to tutorial, check that we saved state in db
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(
            requester.Intent("AMAZON_YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, CONTEXT)
        recipes_result = lambda_function._skill.db_helper.get('recipes')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(len(recipes_result.value), 1)
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertNotEqual(response_dict['sessionAttributes']['current_recipe'], None)
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
        # save current recipe for later in test
        current_recipe = response_dict['sessionAttributes']['current_recipe']

        intent = requester.Intent('IngredientsIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).copy_attributes(
            response_dict).with_intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, CONTEXT)
        state_result = lambda_function._skill.db_helper.getState()
        recipes_result = lambda_function._skill.db_helper.get('recipes')
        current_recipe_result = lambda_function._skill.db_helper.get('current_recipe')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(len(recipes_result.value), 1)
        self.assertEqual(state_result.value, core.States.INGREDIENTS_OR_INSTRUCTIONS)
        self.assertEqual(current_recipe_result.value, current_recipe)
