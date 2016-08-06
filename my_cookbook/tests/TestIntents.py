import unittest
from my_cookbook.util import request
from my_cookbook.util import response
from my_cookbook.skill import main

CONTEXT = {"debug": True}


class IntentTest(unittest.TestCase):
    def single_launch(self):
        r = request.Request()
        event = r.with_type(request.Types.LAUNCH).new().build()
        response = main.handler(event, CONTEXT)

        self.assertTrue(response.is_valid(response))

    def multiple_launch(self):
        r = request.Request().with_type(request.Types.LAUNCH).new()

        for i in range(10):
            event = r.build()
            response = main.handler(event, CONTEXT)
            self.assertTrue(response.is_valid(response))

            r.copy_attributes(response)

