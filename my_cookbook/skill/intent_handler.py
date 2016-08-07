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

        # now we want to try to find a handler fo this intent
        # we first try the exact intent, then that intent without the state
        # then the unhandled intent with the state, and then unhandled without state
        if state in self.handlers:
            if hasattr(self.handlers[state], intent):
                handler_method = getattr(self.handlers[state], intent)
                if handler_method:
                    return handler_method()

        # try intent without state
        elif hasattr(self.handlers[core.States.STATELESS], intent):
            handler_method = getattr(self.handlers[core.States.STATELESS],
                                     intent)
            if handler_method:
                return handler_method()

        # next try Unhandled for that state
        elif state in self.handlers:
            if hasattr(self.handlers[state], intent):
                handler_method = getattr(self.handlers[state], 'Unhandled')
                if handler_method:
                    return handler_method()

        # stateless unhandled is last resort
        elif hasattr(self.handlers[core.States.STATELESS], intent):
            handler_method = getattr(self.handlers[core.States.STATELESS],
                                     'Unhandled')
            if handler_method:
                return handler_method()

        return responder.tell(
            "I'm not sure what you want. Try saying start over.")
