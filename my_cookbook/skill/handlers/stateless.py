import logging

from my_cookbook.util import core
from my_cookbook.util import responder


class StatelessHandler():
    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.NEW_RECIPE], "StartNewRecipeIntent")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def AMAZON_HelpIntent(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.ASK_TUTORIAL], "AMAZON_YesIntent")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def AMAZON_StartOverIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Alright, I've reset everything. I'm ready to start a new recipe.")

    def SessionEndedRequest(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Goodbye.")

    def LaunchRequest(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.INITIAL_STATE], "LaunchRequest")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        if attributes['new']:
            return responder.tell("We've already been talking" \
                " but I have no idea what about, so I will exit this session. Please" \
                " start over by saying, Alexa launch my cookbook.")
        else:
            return responder.tell("Hey, what's up.")


handler = StatelessHandler()
state = core.States.STATELESS
