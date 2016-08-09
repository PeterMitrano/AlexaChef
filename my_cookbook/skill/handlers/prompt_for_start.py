from my_cookbook.util import core
from my_cookbook.util import responder


class PromptForStartHandler:
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.NEW_RECIPE
        return responder.ask(
            "What do you want to make? You can say something like, let's make steak, or how do I cook fried chicken.",
            None, attributes)

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.ask("What can I help you with? Try asking to start a new recipe.", None,
                             attributes)

    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.NEW_RECIPE], "StartNewRecipeIntent")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        pass


handler = PromptForStartHandler()
state = core.States.PROMPT_FOR_START
