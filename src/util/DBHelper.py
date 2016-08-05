from skill import Core
from skill import Response
import boto3

class DBHelper:

  def __init__(self, user, endpoint_url):
    self.user = user
    if endpoint_url:
      self.client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    else:
      self.client = boto3.client("dynamodb")

  def getState(self):
    return self.get(Core.STATE_KEY, 'S')

  def get(self, attribute, attribute_type):
    key = {
      'userId': {
        'S': self.user
      }
    }
    response = self.client.get_item(TableName=Core.DB_TABLE, Key=key)

    try:
      if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        # We're willing to silently fail here in hopes of that being
        # the more pleasent user experience
        return (None, Response.tell("I've forgotten where we were. Please start over"));

      if "Item" not in response:
        # this is fine, it just means we don't have this user yet
        # so we mark that they've used the skill and put them in the db
        print "Adding new user: %s" % self.user
        key['mapAttr'] = {
          'M': {
            'invocations': {
              'N': "1"
            }
          }
        }
        key['mapAttr']['M'][Core.STATE_KEY] = {
          'S': Core.States.INITIAL_STATE
        }
        self.client.put_item(TableName=Core.DB_TABLE, Item=key)

      state = response['Item']['mapAttr']['M'][attribute][attribute_type]
      return (state, None)
    except KeyError:
      return (None, Response.tell("I've forgotten where we were. Please start over"));


