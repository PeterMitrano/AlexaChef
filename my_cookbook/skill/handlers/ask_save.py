from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipes_helper


class AskSaveHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'current_recipe' not in attributes:
            # TODO: ask "which recipe do you want to save
            return responder.tell("I don't know which recipe you want me to save.")

        recipe = attributes['current_recipe']
        recipes_helper.add_recipe(persistant_attributes, recipe)
        return responder.tell("Recipe saved.")

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        # not sure what to do here...? I'm starting to reach the limits of my currentb
        # state machine structure I think
        return responder.tell("Recipe not saved.")

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        return responder.tell("Sorry, I'm not sure what you mean. Do you want to save this recipe?")


handler = AskSaveHandler()
state = core.States.ASK_SAVE
