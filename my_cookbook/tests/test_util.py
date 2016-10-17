import boto3
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

from my_cookbook.util import core
from my_cookbook.util import requester
from my_cookbook.util import dbhelper
from my_cookbook.tests import fake_data
import lambda_function


def delete_table(endpoint_url):
    """deletes the table if it already exists"""
    client = boto3.client(
        "dynamodb",
        endpoint_url=endpoint_url,
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")
    tables = client.list_tables()['TableNames']
    if core.DB_TABLE in tables:
        client.delete_table(TableName=core.DB_TABLE)

def no_firt_time():
    # add a few invocations
    db_helper = dbhelper.DBHelper('default_user_id', core.LOCAL_DB_URI)
    db_helper.init_table()
    db_helper.setAll({'invocations': 1})

def set_bigoven_username():
    client = boto3.client(
        "dynamodb",
        endpoint_url=core.LOCAL_DB_URI,
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")
    client.create_table(
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
    resource = boto3.resource(
        'dynamodb',
        endpoint_url=core.LOCAL_DB_URI,
        region_name="fake_region",
        aws_access_key_id="fake_id",
        aws_secret_access_key="fake_key")
    table = resource.Table('my_cookbook_users')
    table.wait_until_exists()
    item = {"userId": "default_user_id", "bigoven_username": "default_bigoven_username"}
    table.put_item(Item=item)


def wip(f):
    return attr('wip')(f)


def bigoven(f):
    return attr('bigoven')(f)
