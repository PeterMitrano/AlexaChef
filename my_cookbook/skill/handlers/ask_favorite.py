from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipes_helper


class AskFavoriteHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'current_recipe' not in attributes:
            # TODO: ask "which recipe do you want to favorite
            return responder.tell("I don't know which recipe you want me to favorite.")

        recipe = attributes['current_recipe']
        #recipes_helper.favorite_recipe(recipe)
        #return responder.tell("Recipe favorited.")
        raise NotImplementedError()

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        # not sure what to do here...? I'm starting to reach the limits of my currentb
        # state machine structure I think
        return responder.tell("Recipe not favorited.")

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        return responder.tell(
            "Sorry, I'm not sure what you mean. Do you want to favorite this recipe?")


handler = AskFavoriteHandler()
state = core.States.ASK_FAVORITE
