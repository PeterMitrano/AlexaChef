from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipes_helper


class AskMakeOnlineHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        # take the time to download the recipe
        if 'search_recipe_result' not in attributes:
            return responder.tell(
                "I've forgotten which recipe you wanted to make. Please start over")

        name = attributes['search_recipe_result']['Title']
        recipe_id = attributes['search_recipe_result']['RecipeID']
        recipe = recipes_helper.get_online_recipe(attributes['search_recipe_result'])

        if not recipe:
            return responder.tell("Sorry, I couldn't find the recipe %s, with id %s" %
                                  (name, recipe_id))

        attributes['current_recipe'] = recipe

        attributes[core.STATE_KEY] = core.States.INGREDIENTS_OR_INSTRUCTIONS
        return responder.ask("Do you want to start with the ingredients or the instructions?", None,
                             attributes)

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        # search for another recipe online?
        # for now, just give up and reset.
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell(
            "That's all the recipes I know about. Try asking to make something different.")

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused, Do you want to make the recipe from your cookbook?",
                             None, attributes)


handler = AskMakeOnlineHandler()
state = core.States.ASK_MAKE_ONLINE
