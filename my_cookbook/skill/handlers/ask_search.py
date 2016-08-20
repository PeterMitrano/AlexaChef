from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipes_helper


class AskSearchHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        # search for recipe
        if 'current_recipe_name' not in attributes:
            return responder.tell(
                "I'm not sure what recipe you are searching for. Please start over")

        recipe_name = attributes['current_recipe_name']
        recipes = recipes_helper.search_online_recipes(recipe_name)

        if len(recipes) == 0:
            persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
            return responder.tell("I don't know of any recipes for that. Try something else")

        else:
            attributes[core.STATE_KEY] = core.States.ASK_MAKE_ONLINE
            best_guess_recipe_name = recipes[0]['Title']
            attributes['search_recipe_result'] = recipes[0]
            return responder.ask(
                "I found a recipe for " + best_guess_recipe_name + ". Do you want to use that?",
                None, attributes)

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.ASK_SEARCH
        return responder.ask("then what can I do for you?", None, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask(
            "I'm confused, Do you want to search online for a recipe? Try saying yes or no.", None,
            attributes)


handler = AskSearchHandler()
state = core.States.ASK_SEARCH
