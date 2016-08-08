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

    @utils.wip
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
        result = lambda_function._skill.db_helper.getState()
        self.assertEqual(result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)

    @utils.wip
    def test_returning_user(self):
        utils.delete_table(core.LOCAL_DB_URI)

        # first launch on new user should result in a table entry with state set
        # as well as session attributes set correctly
        event = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        self.assertTrue(responder.is_valid(response_dict))
        result = lambda_function._skill.db_helper.get('invocations')
        self.assertEqual(result.value, 1)

        # end the session and make sure database state is good
        event = requester.Request().with_type(requester.Types.END).build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        result = lambda_function._skill.db_helper.getState()
        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)
        result = lambda_function._skill.db_helper.get('invocations')
        self.assertEqual(result.value, 1)

        # on the next request we expect the have the right state
        event = requester.Request().with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)
        result = lambda_function._skill.db_helper.get('invocations')
        self.assertEqual(result.value, 2)
        result = lambda_function._skill.db_helper.getState()
        self.assertEqual(result.value, core.States.INITIAL_STATE)
        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)
