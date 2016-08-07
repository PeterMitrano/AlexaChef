import unittest

from my_cookbook.util import core
from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook.skill import main

CONTEXT = {"debug": True}

class ConversationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.delete_table('http://localhost:8000')

    def test_first_time(self):
        utils.delete_table('http://localhost:8000')

        r = requester.Request()
        event = r.with_type(requester.Types.LAUNCH).new().build()
        skill = main.Skill()
        response_dict = skill.handle_event(event, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))
