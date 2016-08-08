import unittest

from my_cookbook.tests import utils
from my_cookbook.util import requester
from my_cookbook.util import responder


class ResponderTest(unittest.TestCase):
    def test_tell(self):
        response = responder.tell("tell")
        self.assertTrue(responder.is_valid(response))

    def test_ask(self):
        response = responder.ask("ask", None)
        self.assertTrue(responder.is_valid(response))
        response = responder.ask("ask", "reprompt")
        self.assertTrue(responder.is_valid(response))

    def test_tell_card(self):
        response = responder.tell_with_card("tell", "title", "contents", 'http://im.gy/cLK')
        self.assertTrue(responder.is_valid(response))

    def test_ask_card(self):
        response = responder.ask_with_card("tell", None, "title", "contents", 'http://im.gy/cLK')
        self.assertTrue(responder.is_valid(response))
        response = responder.ask_with_card("tell", "reprompt", "title", "contents",
                                           'http://im.gy/cLK')
        self.assertTrue(responder.is_valid(response))
