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
        utils.delete_table(core.LOCAL_DB_URI)

    @utils.wip
    def test_first_time(self):
        utils.delete_table(core.LOCAL_DB_URI)

        r = requester.Request()
        event = r.with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)

        # first launch on new user should result in a table entry with state set
        # as well as session attributes set correctly
        self.assertTrue(responder.is_valid(response_dict))
        logging.getLogger(core.LOGGER).debug(response_dict[
            'sessionAttributes'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INITIAL_STATE)

        result = lambda_function._skill.db_helper.getState()
        self.assertEqual(result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)
