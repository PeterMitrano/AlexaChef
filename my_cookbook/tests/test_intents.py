import unittest

from my_cookbook.util import schema
from my_cookbook.tests import test_util
from my_cookbook.util import core
from my_cookbook.util import requester
from my_cookbook.util import responder
import lambda_function


class IntentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_util.delete_table(core.LOCAL_DB_URI)

    def test_single_launch(self):
        r = requester.Request()
        event = r.type(requester.Types.LAUNCH).new().build()
        response_dict = lambda_function.handle_event(event, None)

        self.assertTrue(responder.is_valid(response_dict))

    def test_multiple_launch(self):
        request = requester.Request().type(requester.Types.LAUNCH).new()

        for i in range(5):
            event = request.build()
            response_dict = lambda_function.handle_event(event, None)
            self.assertTrue(responder.is_valid(response_dict))

    def test_single_end(self):
        r = requester.Request()
        event = r.type(requester.Types.END).new().build()
        response_dict = lambda_function.handle_event(event, None)

        self.assertTrue(responder.is_valid(response_dict))

    def test_multiple_end(self):
        request = requester.Request().type(requester.Types.END).new()

        for i in range(5):
            event = request.build()
            response_dict = lambda_function.handle_event(event, None)
            self.assertTrue(responder.is_valid(response_dict))

    def test_copy_attributes(self):
        request = requester.Request()
        response = responder.tell("test")
        request.copy_attributes(response)
        self.assertEqual(request.request['session']['attributes'], response['sessionAttributes'])

    def test_all_new_intents_in_all_states(self):
        for state in core.all_states():
            for intent_name in schema.intents():
                intent = requester.Intent(intent_name).build()
                event = requester.Request().type(requester.Types.INTENT).new().intent(
                    intent).attributes({core.STATE_KEY: state}).build()
                response_dict = lambda_function.handle_event(event, None)

                self.assertTrue(responder.is_valid(response_dict))

                # make sure the end the conversation
                event = requester.Request().type(requester.Types.END).build()
                response_dict = lambda_function.handle_event(event, None)
                self.assertTrue(responder.is_valid(response_dict))
