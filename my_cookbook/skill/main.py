import logging

from my_cookbook.util import requester
from my_cookbook.util import responder
from my_cookbook.util import core
from my_cookbook.util import dbhelper


def handler(event, context):
    # check if we're debuggin locally
    debug = False
    endpoint_url = None
    if "debug" in context:
        debug = True
        logging.getLogger(core.LOGGER).setLevel(logging.DEBUG)
        endpoint_url = "http://localhost:8000"
    else:
        logging.getLogger(core.LOGGER).setLevel(logging.INFO)

    # check application id and user
    user = event['session']['user']['userId']
    request_appId = event['session']['application']['applicationId']
    if core.APP_ID != request_appId:
        raise Exception('application id %s does not match.' % request_appId)

    # check session attributes and load from DB if needed
    state = ""
    request_attributes = event['session']['attributes']
    if core.STATE_KEY in request_attributes:
        state = request_attributes[core.STATE_KEY]
    else:
        if core.DB_TABLE:
            db_helper = dbhelper.DBHelper(user, endpoint_url)
            db_helper.init_table()
            result = db_helper.getState()

            if result.err:
                return responder.tell(result.error_speech)
            if not result.value:
                state = ""
            else:
                state = result.value
                logging.getLogger(core.LOGGER).debug(
                    "fetched state %s from database" % state)

    # at this point we either know the state, or we have returned an error,
    # or we know it's the users first time and there is no state
    # so now we dispatch
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

    #if stateful_intent in handlers:
#handlers[stateful_intent].handler(slots)
