import logging

from my_cookbook.skill import intent_handler
from my_cookbook.util import responder
from my_cookbook.util import core
from my_cookbook.util import dbhelper

from my_cookbook.skill.handlers import stateless
from my_cookbook.skill.handlers import initial


class Skill:
    def __init__(self):
        self.intent_handler = intent_handler.Handler()
        self.intent_handler.add(stateless.state, stateless.handler)
        self.intent_handler.add(initial.state, initial.handler)

    def handle_event(self, event, context):
        #from nose.tools import set_trace; set_trace()
        # check if we're debuggin locally
        debug = False
        endpoint_url = None
        if "debug" in context:
            debug = True
            logging.getLogger(core.LOGGER).setLevel(logging.DEBUG)
            endpoint_url = core.LOCAL_DB_URI
        else:
            logging.getLogger(core.LOGGER).setLevel(logging.INFO)

        # check application id and user
        user = event['session']['user']['userId']
        request_appId = event['session']['application']['applicationId']
        if core.APP_ID != request_appId:
            raise Exception('application id %s does not match.' %
                            request_appId)

        # check session attributes and load from state DB if needed
        # this also has the effect of ensuring first time users get
        # entered into the database
        state = ""
        request_attributes = event['session']['attributes']
        if core.STATE_KEY in request_attributes:
            state = request_attributes[core.STATE_KEY]
        else:
            if core.DB_TABLE:
                self.db_helper = dbhelper.DBHelper(user, endpoint_url)
                self.db_helper.init_table()
                result = self.db_helper.getState()

                if result.err:
                    return responder.tell(
                        result.
                        error_speech)  #TODO: do I need to copy request_attributes here?
                if not result.value:
                    state = ""
                else:
                    state = result.value
                    logging.getLogger(core.LOGGER).debug(
                        "fetched state %s from database" % state)

        # at this point we either know the state, or we have returned an error,
        # or we know it's the users first time and there is no state
        # so now we dispatch
        return self.intent_handler.dispatch(state, request_attributes, event)
