import boto3
from functools import wraps
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

from my_cookbook.util import core


def delete_table(endpoint_url):
    """deletes the table if it already exists"""
    client = boto3.client(
        "dynamodb",
        endpoint_url=self.endpoint_url,
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")
    tables = client.list_tables()['TableNames']
    if core.DB_TABLE in tables:
        client.delete_table(TableName=core.DB_TABLE)


def wip(f):
    return attr('wip')(f)
