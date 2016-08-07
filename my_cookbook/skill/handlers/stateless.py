import logging

from my_cookbook.util import core
from my_cookbook.util import responder


class StateHandler():
    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes,
                             slots):
        handler = getattr(handlers[core.States.NEW_RECIPE],
                          "StartNewRecipeIntent")
        return handler(attributes, slots)

    def AMAZON_HelpIntent(self, handlers, persistant_attributes, attributes,
                          slots):
        attributes[core.STATE_KEY] = core.States.ASK_TUTORIAL
        return responder.ask("AMAZON.YesIntent" + core.States.ASK_TUTORIAL,
                             attributes)

    def AMAZON_StartOverIntent(self, handlers, persistant_attributes,
                               attributes, slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.ask(
            ":ask",
            "Alright, I've reset everything. I'm ready to start a new recipe.",
            attributes)

    def SessionEndedRequest(self, handlers, persistant_attributes, attributes,
                            slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.ask(":tell", "Goodbye.", attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.ask(":tell", "We've already been talking" \
            " but I have no idea what about, so I will exit this session. Please" \
            " start over by saying, Alexa launch my cookbok.", attributes)


handler = StateHandler()
state = core.States.STATELESS
