import boto3
from collections import namedtuple
import logging

from my_cookbook.util import core
from my_cookbook.util import responder

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('nose').setLevel(logging.WARNING)


class DBHelper:
    def __init__(self, user, endpoint_url):
        self.endpoint_url = endpoint_url
        self.user = user
        if endpoint_url:
            self.dynamodb = boto3.resource(
                "dynamodb",
                endpoint_url=endpoint_url,
                region_name="fake_region",
                aws_access_key_id="fake_id",
                aws_secret_access_key="fake_key")
        else:
            self.dynamodb = boto3.resource("dynamodb")

    def init_table(self):
        # check if table exists, and if it doesn't then create it
        # and wait for it to be ready
        self.client = boto3.client("dynamodb", endpoint_url=self.endpoint_url)
        tables = self.client.list_tables()['TableNames']

        if core.DB_TABLE not in tables:
            self.table = self.client.create_table(
                TableName=core.DB_TABLE,
                KeySchema=[
                    {
                        'AttributeName': 'userId',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'userId',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                })
            self.client.get_waiter('table_exists').wait(
                TableName=core.DB_TABLE)

        # at this point we know the table is there
        self.table = self.dynamodb.Table(core.DB_TABLE)

    def getAll(self):
        """get all values of attribute, return tuple of (truthy error, value dict, error speech"""
        result = namedtuple('result', ['err', 'value', 'error_speech'])
        key = {'userId': self.user}

        if not self.table:
            logging.getLogger(core.LOGGER).warn("Did you call init_table?")
            return result(
                True, None,
                'I cannot reach my database right now. I would try again later.')

        response = self.table.get_item(Key=key)

        try:
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return result(
                    True, None,
                    'I cannot reach my database right now. I would try again later.')

            if "Item" not in response:
                # this is fine, it just means we don't have this user yet
                # so we mark that they've used the skill and put them in the db
                logging.getLogger(core.LOGGER).info("Adding new user: %s" %
                                                    self.user)
                item = {
                    'userId': self.user,
                    'invocations': 1,
                    core.STATE_KEY: core.States.INITIAL_STATE
                }
                self.table.put_item(Item=item)

                # this is an not error, so you better check for None as value
                return result(False, None,
                              'This must be your first time. Welcome!')

            return result(False, response['Item'], None)
        except KeyError:
            return result(True, None,
                          "I've forgotten where we were. Please start over")

    def setState(self, state):
        return self.set(core.STATE_KEY, state)

    def getState(self):
        """ Get values from the attribute of an item return tuple of (truthy error, value, error speech)"""
        return self.get(core.STATE_KEY)

    def set(self, attribute, value):
        """ Set attribute of an item return tuple of (truthy error, error speech)

        This will also create the user if they don't exist
        """
        result = namedtuple('result', ['err', 'error_speech'])
        key = {'userId': self.user}
        updateExpr = 'SET %s = :attr' % attribute
        exprAttributeValues = {':attr': value}

        if not self.table:
            logging.getLogger(core.LOGGER).warn("Did you call init_table?")
            return result(
                True,
                'I cannot reach my database right now. I would try again later.')

        response = self.table.update_item(
            Key=key,
            UpdateExpression=updateExpr,
            ExpressionAttributeValues=exprAttributeValues)

        try:
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return result(
                    True,
                    'I cannot reach my database right now. I would try again later.')

            if "Item" not in response:
                # this isn't actually an error
                return result(False, 'This must be your first time. Welcome!')

            state = response['Item'][attribute]
            return result(False, None)
        except KeyError:
            return result(True, 'Keyerror')

    def get(self, attribute):
        """ Get values from the attribute of an item return tuple of (truthy error, value, error speech)

        This will also create the user if they dont exist
        """

        result = namedtuple('result', ['err', 'value', 'error_speech'])
        get = self.getAll()
        if isinstance(get.value, dict):
            if attribute in get.value:
                return result(False, get.value[attribute], None)
        else:
            # this means something really went wrong, or the user is new
            if get.err:
                return result(True, None, get.error_speech)
            else:
                return result(False, None, get.error_speech)
