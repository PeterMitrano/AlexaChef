from my_cookbook.util import core
from my_cookbook.util import responder


class AskMakeCookbookHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INGREDIENTS_OR_INSTRUCTIONS
        return responder.ask("Do you want to start with the ingredients or the instructions?", None,
                             attributes)

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.ASK_SEARCH
        return responder.ask("I could search for one online?", None, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused, Do you want to make the recipe from your cookbook?",
                             None, attributes)


handler = AskMakeCookbookHandler
state = core.States.ASK_MAKE_COOKBOOK
