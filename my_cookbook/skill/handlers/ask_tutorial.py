from my_cookbook.util import core
from my_cookbook.util import responder


class AskTutorialHandler:
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        return responder.tell(
            "I am capable of finding recipes and walking you through making them. Try asking how to make pancakes")

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.PROMPT_FOR_START
        return responder.ask(
            "Are you ready to start making something? You can say yes, or ask me something else.",
            None, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask(
            "I'm confused. Do you want to start with a tutorial? Try saying yes or no.", None,
            attributes)


handler = AskTutorialHandler()
state = core.States.ASK_TUTORIAL
