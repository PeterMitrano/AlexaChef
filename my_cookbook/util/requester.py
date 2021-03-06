import logging

from my_cookbook.util import core


class Types:
    LAUNCH = 'LaunchRequest'
    INTENT = 'IntentRequest'
    END = 'SessionEndedRequest'


class Intent():
    def __init__(self, name):
        self.intent = {"name": name}

    def slot(self, name, value):
        self.intent['slots'] = {name: {"name": name, "value": value}}
        return self

    def build(self):
        return self.intent


class Request():
    def __init__(self):
        self.request = {
            "version": "1.0",
            "session": {
                "application": {
                    "applicationId": core.APP_ID
                },
                "sessionId": "default_session_id",
                "new": False,
                "user": {
                    "userId": "default_user_id"
                }
            },
            "request" : {
            }
        }

    def copy_attributes(self, response):
        attrs = response['sessionAttributes']
        logging.getLogger(core.LOGGER).debug('attrs: %s' % attrs)
        return self.attributes(attrs)

    def app_id(self, app_id):
        self.request['session']['application']['applicationId'] = app_id
        return self

    def attributes(self, attributes):
        self.request['session']['attributes'] = attributes
        return self

    def new(self):
        self.request['session']['new'] = True
        return self

    def type(self, request_type):
        self.request['request']['type'] = request_type
        return self

    def user(self, userId):
        self.request['session']['user']['userId'] = userId
        return self

    def intent(self, intent):
        self.request['request']['intent'] = intent
        return self

    def build(self):
        return self.request
