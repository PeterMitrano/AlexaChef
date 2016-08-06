import unittest

from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook.skill import main

CONTEXT = {"debug": True}


class IntentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        utils.delete_table('http://localhost:8000')

    @utils.wip
    def test_single_launch(self):
        r = requester.Request()
        event = r.with_type(requester.Types.LAUNCH).new().build()
        skill = main.Skill()
        response_dict = skill.handle_event(event, CONTEXT)

        self.assertTrue(responder.is_valid(response_dict))

    @utils.wip
    def test_multiple_launch(self):
        request = requester.Request().with_type(requester.Types.LAUNCH).new()

        for i in range(10):
            event = request.build()
            skill = main.Skill()
            response_dict = skill.handle_event(event, CONTEXT)
            self.assertTrue(responder.is_valid(response_dict))

            request.copy_attributes(response_dict)
