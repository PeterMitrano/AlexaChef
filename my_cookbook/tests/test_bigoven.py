import unittest

from my_cookbook import stage
from my_cookbook.util import core
from my_cookbook.tests import test_util
from my_cookbook.util import recipes_helper
from my_cookbook.util import requester
from my_cookbook.util import responder
import requests
import lambda_function


class KeyTest(unittest.TestCase):
    def test_key(self):
        core.load_key()
        self.assertTrue(True)


class APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.BIGOVEN = True

    @classmethod
    def tearDownClass(cls):
        core.BIGOVEN = False

    @test_util.bigoven
    def test_search_recipes(self):
        recipes = recipes_helper.search_online_recipes("chocolate fondue")
        self.assertGreater(len(recipes), 10)

        recipes = recipes_helper.search_online_recipes("kentucky fried chicken")
        self.assertGreater(len(recipes), 10)

    @test_util.bigoven
    def test_search_user_recipes(self):
        recipes = recipes_helper.search_my_recipes("pancakes", '_test')
        self.assertEqual(len(recipes), 4)

        recipes = recipes_helper.search_my_recipes("jalapeno poppers", '_test')
        self.assertEqual(len(recipes), 1)


class LinkTest(unittest.TestCase):
    @test_util.bigoven
    def test_make_link(self):
        test_util.delete_table(core.LOCAL_DB_URI)
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName',
                                                                    'chicken pot pie').build()
        req = requester.Request().new().with_type(requester.Types.INTENT).with_intent(intent).build(
        )
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))

        #fake the user entering their id
        fake_bigoven_username = 'bigoven_test_user'
        response = requests.get(
            'http://localhost:5000/link?amazonId=default_user_id&bigoven_username=%s' %
            fake_bigoven_username)
        self.assertTrue(response.ok)

        link_result = lambda_function._skill.db_helper.get('bigoven_username')
        self.assertEqual(link_result.value, fake_bigoven_username)


class RealRecipeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.BIGOVEN = True

    @classmethod
    def tearDownClass(cls):
        core.BIGOVEN = False

    @test_util.bigoven
    @test_util.wip
    def test_brownies(self):
        test_util.delete_table(core.LOCAL_DB_URI)
        test_util.set_bigoven_username()

        # search for something not in our cookbook
        intent = requester.Intent('StartNewRecipeIntent').with_slot('RecipeName',
                                                                    'brownies').build()
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(intent).new().build(
        )
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe_name', response_dict['sessionAttributes'])
        self.assertEqual(response_dict['sessionAttributes']['current_recipe_name'], 'brownies')
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY], core.States.ASK_SEARCH)

        # response with "Yes" to search online
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('search_recipe_result', response_dict['sessionAttributes'])
        self.assertIn('Title', response_dict['sessionAttributes']['search_recipe_result'])
        self.assertIn('RecipeID', response_dict['sessionAttributes']['search_recipe_result'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.ASK_MAKE_ONLINE)

        # response with "Yes" to make the recipe it found
        req = requester.Request().with_type(requester.Types.INTENT).with_intent(
            requester.Intent("AMAZON.YesIntent").build()).copy_attributes(response_dict).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertIn('current_recipe', response_dict['sessionAttributes'])
        self.assertIn('Title', response_dict['sessionAttributes']['current_recipe'])
        self.assertIn('RecipeID', response_dict['sessionAttributes']['current_recipe'])
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)

        # ask for ingredients
        intent = requester.Intent('IngredientsIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).copy_attributes(
            response_dict).with_intent(intent).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)

        # now ask for instructions
        intent = requester.Intent('InstructionsIntent').build()
        req = requester.Request().with_type(requester.Types.INTENT).copy_attributes(
            response_dict).with_intent(intent).build()
        response_dict = lambda_function.handle_event(req, None)

        self.assertTrue(responder.is_valid(response_dict))
        self.assertEqual(response_dict['sessionAttributes'][core.STATE_KEY],
                         core.States.INGREDIENTS_OR_INSTRUCTIONS)
