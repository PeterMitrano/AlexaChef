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
        utils.delete_table('http://localhost:8000')

    @utils.wip
    def test_first_time(self):
        utils.delete_table('http://localhost:8000')

        r = requester.Request()
        event = r.with_type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, CONTEXT)

        result = lambda_function._skill.db_helper.getState()

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(result.value, core.States.INITIAL_STATE)
        self.assertEqual(lambda_function._skill.db_helper.table.item_count, 1)
        #self.assertEqual(response_dict['response']['outputSpeech']['ssml'],
