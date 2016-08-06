import logging
from my_cookbook.util import core
from my_cookbook.util import responder


class Handler():
    def handle(self, intent, slots):
        logging.getLogger(core.LOGGER).debug("initial: %r", slots)


handler = Handler()
state = core.States.INITIAL_STATE
