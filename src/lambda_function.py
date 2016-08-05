from skill import Response
from skill import Core
from util.DBHelper import DBHelper

def lambda_handler(event, context):
  # check if we're debuggin locally
  debug = False
  endpoint_url = None
  if "debug" in context:
    debug = True
    endpoint_url = "http://localhost:8000"

  # check application id and user
  user = event['session']['user']['userId']
  request_appId = event['session']['application']['applicationId']
  if Core.appId != request_appId:
    raise Exception('application id %s does not match.' % request_appId)

  # check session attributes and load from DB if needed
  state = ""
  request_attributes = event['session']['attributes']
  if Core.STATE_KEY in request_attributes:
    state = request_attributes[Core.STATE_KEY]
  else:
    if Core.DB_TABLE:
      db_helper = DBHelper(user, endpoint_url)
      (state, error_response) = db_helper.getState()

      if error_response:
        return error_response

  # at this point we either know the state, or we have returned an error



