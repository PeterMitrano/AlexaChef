import unittest

from my_cookbook.util import core
from my_cookbook.tests import test_util


class BigOvenTest(unittest.TestCase):
    def test_key(self):
        core.load_key()
        self.assertTrue(True)
