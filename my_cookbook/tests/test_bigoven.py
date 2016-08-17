import unittest

from my_cookbook.util import core
from my_cookbook import stage
from my_cookbook.util import recipes_helper
from my_cookbook.tests import test_util


class KeyTest(unittest.TestCase):
    def test_key(self):
        core.load_key()
        self.assertTrue(True)

class APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stage.PROD = True

    @classmethod
    def tearDownClass(cls):
        stage.PROD = False

    @test_util.bigoven
    def test_search_recipes(self):
        recipes = recipes_helper.search_online_recipes("buttermilk pancakes")
        self.assertGreater(len(recipes), 10)

        recipes = recipes_helper.search_online_recipes("soft shell chicken tacos")
        self.assertGreater(len(recipes), 10)

        recipes = recipes_helper.search_online_recipes("chocolate fondue")
        self.assertGreater(len(recipes), 10)

        recipes = recipes_helper.search_online_recipes("kentucky fried chicken")
        self.assertGreater(len(recipes), 10)
