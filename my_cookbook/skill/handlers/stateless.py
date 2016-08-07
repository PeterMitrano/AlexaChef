import logging

from my_cookbook.util import core
from my_cookbook.util import responder


class StateHandler():
    def StartNewRecipeIntent(self, handlers, attributes, slots):
        handler = getattr(handlers[core.States.NEW_RECIPE],
                          "StartNewRecipeIntent")
        return handler(attributes, slots)

    def AMAZON_HelpIntent(self, attributes, slots):
        self.handler.state = core.States.ASK_TUTORIAL
        return responder.ask("AMAZON.YesIntent" + core.States.ASK_TUTORIAL)

    def AMAZON_StartOverIntent(self, attributes, slots):
        self.handler.state = core.States.INITIAL_STATE
        return responder.ask(
            ":ask",
            "Alright, I've reset everything. I'm ready to start a new recipe.")

    def SessionEndedRequest(self, attributes, slots):
        self.handler.state = core.States.INITIAL_STATE
        return responder.ask(":tell", "Goodbye.")
        return responder.ask(":saveState", true)

    def Unhandled(self, attributes, slots):
        self.handler.state = core.States.INITIAL_STATE
        return responder.ask(
            ":tell",
            "We've already been talking but I have no idea what about, so I will exit self session. Please start over by saying, Alexa launch my cookbok.")
        return responder.ask(":saveState", true)


handler = StateHandler()
state = core.States.STATELESS
