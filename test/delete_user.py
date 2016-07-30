#!/usr/bin/python

import boto3
import click
import json

@click.command()
@click.option("--userid", default="user0", help="delete this user from the my_cookbook_users table")
def delete_user(userid):
    dynamo_client = boto3.client('dynamodb')
    key = {"userId": {"S" : userid}}
    dynamo_client.delete_item(TableName="my_cookbook_users", Key=key)

if __name__ == "__main__":
    delete_user()
