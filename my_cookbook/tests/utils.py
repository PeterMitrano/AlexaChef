import boto3
from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

from my_cookbook.util import core


def delete_table(endpoint_url):
    """deletes the table if it already exists"""
    client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    tables = client.list_tables()['TableNames']
    if core.DB_TABLE in tables:
        client.delete_table(TableName=core.DB_TABLE)


def wip(f):
    return attr('wip')(f)
