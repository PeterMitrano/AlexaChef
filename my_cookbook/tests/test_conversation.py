import logging
import unittest

from my_cookbook.util import core
from my_cookbook.tests import test_util
from my_cookbook.util import requester
from my_cookbook.util import responder
import lambda_function


class ConversationTest(unittest.TestCase):
    def test_first_time(self):
        test_util.delete_table(core.LOCAL_DB_URI)

        event = requester.Request().type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, None)

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
        test_util.delete_table(core.LOCAL_DB_URI)

        # first launch on new user should result in a table entry with state set
        # as well as session attributes set correctly
        event = requester.Request().type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, None)
        inv_result = lambda_function._skill.db_helper.get('invocations')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 1)

        # end the session and make sure database state is good
        event = requester.Request().type(requester.Types.END).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(event, None)
        inv_result = lambda_function._skill.db_helper.get('invocations')
        state_result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 1)
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

        # on the next request we expect the have the right state
        # last response was a tell, so we don't need to call copy_attributes
        r = requester.Request()
        event = r.type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, None)
        inv_result = lambda_function._skill.db_helper.get('invocations')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(inv_result.value, 2)
        self.assertFalse(response_dict['response']['shouldEndSession'])
        self.assertEqual(response_dict['sessionAttributes']['STATE'], core.States.NEW_RECIPE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

    def test_tutorial_conversation(self):
        test_util.delete_table(core.LOCAL_DB_URI)

        # lauch as new user, check out session attributes are in ASK_TUTORIAL
        req = requester.Request().type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_TUTORIAL)

        # response with "Yes" to to tutorial, check that we saved state in db
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("_MAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)
        state_result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(state_result.value, core.States.INITIAL_STATE)

        # delete user so we are prompted again, this time respond no.
        test_util.delete_table(core.LOCAL_DB_URI)

        # lauch as new user again
        req = requester.Request().type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(req, None)

        # response with "No" to to tutorial, check that we saved state in db
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("AMAZON.NoIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.PROMPT_FOR_START)

    @test_util.wip
    def test_launch_recipe_conversation(self):
        test_util.delete_table(core.LOCAL_DB_URI)
        test_util.set_bigoven_username()

        event = requester.Request().type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, None)
        inv_result = lambda_function._skill.db_helper.get('invocations')

        self.assertTrue(responder.is_valid(response_dict))
        self.assertFalse(response_dict['response']['shouldEndSession'])
        self.assertEqual(inv_result.value, 1)

        # lauch as new user, check out session attributes afterwards
        intent = requester.Intent('StartNewRecipeIntent').slot('RecipeName',
                                                               'chicken pot pie').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)

        # response with "Yes" to make recipe from cookbook, check that we saved state in db
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertNotEqual(response_dict['sessionAttributes']['current_recipe'], None)
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
        # save current recipe for later in test
        current_recipe = response_dict['sessionAttributes']['current_recipe']

        # ask for ingredients
        intent = requester.Intent('IngredientsIntent').build()
        req = requester.Request().type(requester.Types.INTENT).copy_attributes(
            response_dict).intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
        self.assertEqual(response_dict['sessionAttributes']['current_recipe'], current_recipe)

    def test_recipe_conversation(self):
        test_util.delete_table(core.LOCAL_DB_URI)
        test_util.set_bigoven_username()

        # lauch as new user, check out session attributes afterwards
        intent = requester.Intent('StartNewRecipeIntent').slot('RecipeName',
                                                               'chicken pot pie').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_COOKBOOK)

        # response with "Yes" to make recipe from cookbook, check that we saved state in db
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertNotEqual(response_dict['sessionAttributes']['current_recipe'], None)
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
        # save current recipe for later in test
        current_recipe = response_dict['sessionAttributes']['current_recipe']

        # ask for ingredients
        intent = requester.Intent('IngredientsIntent').build()
        req = requester.Request().type(requester.Types.INTENT).copy_attributes(
            response_dict).intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
        self.assertEqual(response_dict['sessionAttributes']['current_recipe'], current_recipe)

    def test_search_one_match_conversation(self):
        test_util.delete_table(core.LOCAL_DB_URI)
        test_util.set_bigoven_username()

        # lauch as new user, check out session attributes afterwards
        # since there are no recipes in our cookbook it should search
        # but we expect "pancakes" to be one of the recipes in the online database
        intent = requester.Intent('StartNewRecipeIntent').slot('RecipeName', 'pizza').build()
        req = requester.Request().type(requester.Types.INTENT).intent(intent).new().build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe_name', response_dict['sessionAttributes'])
        # save current recipe for later in test
        current_recipe_name = response_dict['sessionAttributes']['current_recipe_name']
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

        # response with "Yes" to search
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('search_recipe_result', response_dict['sessionAttributes'])
        self.assertNotEqual(response_dict['sessionAttributes']['search_recipe_result']['Title'],
                            None)
        self.assertEqual(current_recipe_name, 'pizza')
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_ONLINE)

        # response with "Yes" to use the recipe we found
        req = requester.Request().type(requester.Types.INTENT).intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertNotEqual(response_dict['sessionAttributes']['current_recipe'], None)
        self.assertEqual(current_recipe_name, 'pizza')
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
