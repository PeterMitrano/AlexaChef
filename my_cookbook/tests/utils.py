from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

def wip(f):
    return attr('wip')(f)
