import logging
import random
import time
import unittest

from my_cookbook.tests import utils
from my_cookbook.util import core
from my_cookbook.util import dbhelper


class DBHelperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint_url = core.LOCAL_DB_URI
        cls.db_helper = dbhelper.DBHelper(None, cls.endpoint_url)

    def test_new_user(self):
        utils.delete_table(self.endpoint_url)
        self.db_helper.init_table()

        result = self.db_helper.set("test_attr", 1)
        self.assertFalse(result.err)

        result = self.db_helper.get("test_attr")
        self.assertFalse(result.err)
        self.assertEqual(result.value, 1)
        self.assertEqual(self.db_helper.table.item_count, 1)

    def test_many_new_users(self):
        utils.delete_table(self.endpoint_url)
        self.db_helper.init_table()
        self.assertEqual(self.db_helper.table.item_count, 0)

        N_USERS = 100
        for i in range(N_USERS):
            self.db_helper.user = 'new_user_%i' % i
            result = self.db_helper.set("test_attr", 1)
            self.assertFalse(result.err)

            result = self.db_helper.get("test_attr")
            self.assertFalse(result.err)
            self.assertEqual(result.value, 1)

        self.assertEqual(self.db_helper.table.item_count, N_USERS)

    def test_get_all(self):
        self.db_helper.user = 'new_user_%i' % random.randint(0,1000)
        self.db_helper.init_table()

        result = self.db_helper.set("key_a", 1)
        self.assertFalse(result.err)
        result = self.db_helper.set("key_b", "2")
        self.assertFalse(result.err)
        result = self.db_helper.set("key_c", False)
        self.assertFalse(result.err)

        result = self.db_helper.getAll()
        self.assertFalse(result.err)
        self.assertEqual(result.value['key_a'], 1)
        self.assertEqual(result.value['key_b'], "2")
        self.assertEqual(result.value['key_c'], False)
