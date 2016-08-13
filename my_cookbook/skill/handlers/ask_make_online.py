from my_cookbook.util import core
from my_cookbook.util import responder


class AskMakeOnlineHandler():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INGREDIENTS_OR_INSTRUCTIONS
        return responder.ask("Do you want to start with the ingredients or the instructions?", None,
                             attributes)

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        # search for another recipe online?
        # for now, just give up and reset.
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Well that's all the recipes I know about. Try asking to make something different.")

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused, Do you want to make the recipe from your cookbook?",
                             None, attributes)


handler = AskMakeOnlineHandler()
state = core.States.ASK_MAKE_ONLINE
