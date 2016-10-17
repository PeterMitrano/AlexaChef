import logging
from my_cookbook.util import core
from my_cookbook.util import responder


class InitialHandler():
    def SessionEndedRequest(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Goodbye.")

    def LaunchRequest(self, handlers, persistant_attributes, attributes, slots):
        if persistant_attributes['invocations'] == 1:  # first time! Say hello!
            attributes[core.STATE_KEY] = core.States.ASK_TUTORIAL
            return responder.ask(
                "Hi, I'm your new cookbook. Would you like start off with a tutorial?", None,
                attributes)
        else:
            if attributes['new']:
                attributes[core.STATE_KEY] = core.States.NEW_RECIPE
                return responder.ask("Welcome back. What would you like to make?", None, attributes)
            else:
                persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
                return responder.tell("I've already been launched.")

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("We've already been talking" \
            " but I have no idea what about, so I will exit this session. Please" \
            " start over by saying, Alexa launch my cookbok.")


handler = InitialHandler()
state = core.States.INITIAL_STATE
