import logging
import unittest

from my_cookbook.util import core
from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook import lambda_function

CONTEXT = {"debug": True}


class ConversationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # remember since we're using the lambda_function, which goes through
        # main, we will be using the `default_user_id` for everything
        utils.delete_table(core.LOCAL_DB_URI)

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

    def test_help_intent(self):
        # test that help command works in all states
        for state in core.all_states():
            req = requester.Request().with_type(requester.Types.INTENT).with_attributes(
                {core.STATE_KEY: state}).with_intent(requester.Intent("AMAZON_HelpIntent").build(
                )).build()
            response_dict = lambda_function.handle_event(req, CONTEXT)
            state_result = lambda_function._skill.db_helper.getState()

            self.assertTrue(responder.is_valid(response_dict))
            self.assertEqual(state_result.value, core.States.INITIAL_STATE)

            # make sure the end the conversation
            event = requester.Request().with_type(requester.Types.END).build()
            response_dict = lambda_function.handle_event(event, CONTEXT)
            self.assertTrue(responder.is_valid(response_dict))
