import logging

from my_cookbook.util import core
from my_cookbook.util import requester
from my_cookbook.util import responder


class Handler:
    def __init__(self):
        self.handlers = {}

    def add(self, state, handler):
        self.handlers[state] = handler

    def dispatch(self, state, attributes, event):
        request_type = event['request']['type']
        intent = ""
        slots = {}

        if request_type == requester.Types.LAUNCH:
            intent = requester.Types.LAUNCH
        elif request_type == requester.Types.INTENT:
            slots = event['request']['intent']['slots']
            intent = requester.Types.INTENT
        elif request_type == requester.Types.END:
            intent = requester.Types.END
        else:
            return responder.tell(
                "I'm not sure what your intent is. Try asking differently")

        stateful_intent = intent + state

        # this dict will be filled & modified by the various intent
        # handlers, and then we will save it to the database for them
        presistant_attributes = {}

        # now we want to try to find a handler fo this intent
        # we first try the exact intent, then that intent without the state
        # then the unhandled intent with the state, and then unhandled without state
        if state in self.handlers:
            if hasattr(self.handlers[state], intent):
                handler_method = getattr(self.handlers[state], intent)
                logging.getLogger(core.LOGGER).info(
                    "found handler for stateful intent")
                return handler_method(self.handlers, attributes, slots)

        # try intent without state
        if hasattr(self.handlers[core.States.STATELESS], intent):
            handler_method = getattr(self.handlers[core.States.STATELESS],
                                     intent)
            logging.getLogger(core.LOGGER).info(
                "found handler for stateless intent")
            return handler_method(self.handlers, attributes, slots)

        # next try Unhandled for that state
        if state in self.handlers:
            if hasattr(self.handlers[state], intent):
                handler_method = getattr(self.handlers[state], 'Unhandled')
                logging.getLogger(core.LOGGER).info(
                    "found handler for stateful unhandled")
                return handler_method(self.handlers, attributes, slots)

        # stateless unhandled is last resort
        if hasattr(self.handlers[core.States.STATELESS], 'Unhandled'):
            handler_method = getattr(self.handlers[core.States.STATELESS],
                                     'Unhandled')
            logging.getLogger(core.LOGGER).info(
                "found handler for stateless unhandled")
            return handler_method(self.handlers, attributes, slots)

        logging.getLogger(core.LOGGER).info("found no handlers")
        return responder.tell(
            "I'm not sure what you want. Try saying start over.")
