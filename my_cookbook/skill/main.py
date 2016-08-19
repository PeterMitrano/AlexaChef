import copy
import logging
import os

from my_cookbook import stage
from my_cookbook.skill import intent_handler
from my_cookbook.util import responder
from my_cookbook.util import core
from my_cookbook.util import dbhelper
import my_cookbook.skill.handlers as handlers

import pkgutil


class Skill:
    def __init__(self):
        self.intent_handler = intent_handler.Handler()

        # automagically add all the handlers
        for importer, modname, _ in pkgutil.iter_modules(handlers.__path__):
            handler_mod = importer.find_module(modname).load_module(modname)
            self.intent_handler.add(handler_mod.state, handler_mod.handler)

    def handle_event(self, event, context):
        # check if we're debugging locally
        if stage.PROD:
            debug = False
            endpoint_url = None
            logging.getLogger(core.LOGGER).setLevel(logging.INFO)
        else:
            debug = True
            logging.getLogger(core.LOGGER).setLevel(logging.DEBUG)
            endpoint_url = core.LOCAL_DB_URI

        # check application id and user
        user = event['session']['user']['userId']
        request_appId = event['session']['application']['applicationId']
        if core.APP_ID != request_appId:
            raise Exception('application id %s does not match.' % request_appId)

        # store session attributes so the various handlers know what's up
        if 'attributes' in event['session']:
            session_attributes = event['session']['attributes']
        else:
            session_attributes = {}

        # try to pull the current values from the database so we can initialize
        # the persistant_attributes dict. This will also create the user if they
        # do not exist
        self.db_helper = dbhelper.DBHelper(user, endpoint_url)
        self.db_helper.init_table()
        result = self.db_helper.getAll()

        persistant_attributes = {}
        if result.value:  #user at least exists
            persistant_attributes = result.value
            # but we don't want to save the userId so pop that
            persistant_attributes.pop('userId', None)


        initial_persistant_attributes = copy.deepcopy(persistant_attributes)

        # next try to figure out the current state. Look in the event first
        # and if that fails check our database via the persistant_attributes we just got
        state = ""
        if core.STATE_KEY in session_attributes:
            state = session_attributes[core.STATE_KEY]
        elif core.STATE_KEY in persistant_attributes:
            state = persistant_attributes[core.STATE_KEY]

        # increment invocations if this is a new session. invocations is used
        # to improve VUI because we know how many times the user has used the skill
        if event['session']['new']:
            if 'invocations' in persistant_attributes:
                persistant_attributes['invocations'] += 1
            else:
                persistant_attributes['invocations'] = 1

        # add whether the request is 'new' into the attributes for conveneince
        # and make sure state is in session_attributes, not persistant attributes
        session_attributes['new'] = event['session']['new']
        session_attributes['user'] = user

        # at this point we either know the state, or we have returned an error,
        # or we know it's the users first time and there is no state
        # so now we dispatch
        response = self.intent_handler.dispatch(state, persistant_attributes, session_attributes,
                                                event)

        # now that we're done, we need to favorite the recipe
        # the persistant_attributes dict to our database
        # but only do it if something change
        if persistant_attributes != initial_persistant_attributes:
            self.db_helper.setAll(persistant_attributes)

        # don't delete this or you can't debug production
        logging.getLogger(core.LOGGER).warn(response)

        # ok we're finally done
        return response
