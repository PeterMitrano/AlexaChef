import logging
import random
from my_cookbook.util import core
from my_cookbook.util import responder


class NewRecipeHandler():
    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'RecipeName' not in slots:
            return responder.ask(
                "I couldn't figure what recipe you wanted. Try saying, How do I make pancakes?",
                'Try saying, How do I make pancakes?', attributes)
        else:
            recipe_name = slots['RecipeName']
            # here we make an API call and find out if the user has a recipe for this already or not.
            user_has_recipe = random.randint(0, 1) > 0  #TODO: make api call, for now it's random
            if user_has_recipe:
                attributes[core.STATE_KEY] = core.States.ASK_MAKE_COOKBOOK
                return responder.ask("I found a recipe for " + recipe_name +
                                     ", In your cookbook. Do you want to use that?", None,
                                     attributes)
            else:
                attributes[core.STATE_KEY] = core.States.ASK_SEARCH
                return responder.ask("I didn't find any recipe for " + recipe_name +
                                     ", In your cookbook. Should I find one online?",
                                     "Do you want to find another recipe?", attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused. Try asking me what you want to make.", None, attributes)


handler = NewRecipeHandler()
state = core.States.NEW_RECIPE
