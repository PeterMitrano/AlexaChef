import boto3
import logging
import random
import time
import unittest

from my_cookbook.tests import utils
from my_cookbook.util import core
from my_cookbook.util import dbhelper

def delete_table(endpoint_url):
    """deletes the table if it already exists"""
    client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    tables = client.list_tables()['TableNames']
    if core.DB_TABLE in tables:
        client.delete_table(TableName=core.DB_TABLE)

class DBHelperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint_url = 'http://localhost:8000'
        delete_table(cls.endpoint_url)
        cls.db_helper = dbhelper.DBHelper(None, cls.endpoint_url)
        cls.db_helper.init_table()

    def test_new_user(self):
        user = 'new_user_' + str(random.randint(0, 1000))

        result = self.db_helper.set("test_attr", 1)
        self.assertFalse(result.err)

        result = self.db_helper.get("test_attr")
        self.assertFalse(result.err)
        self.assertEqual(result.value, 1)

    def test_many_new_users(self):
        user = 'new_user_' + str(random.randint(0, 1000))

        for i in range(100):
            self.db_helper.user = 'new_user_' + str(random.randint(0, 1000))
            result = self.db_helper.set("test_attr", 1)
            self.assertFalse(result.err)

            result = self.db_helper.get("test_attr")
            self.assertFalse(result.err)
            self.assertEqual(result.value, 1)
