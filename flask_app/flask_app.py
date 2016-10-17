import boto3
from dotenv import load_dotenv
import json
import os
from os.path import join, dirname
from botocore.exceptions import ClientError
from flask import Flask, render_template, request

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

@app.route('/')
def root():
    amazonId = request.args.get('amazonId')
    return render_template('index.html', amazonId=amazonId)

@app.route('/link')
def link():
    amazonId = request.args.get('amazonId')
    bigoven_username = request.args.get('bigoven_username')

    if app.debug:
        resource = boto3.resource('dynamodb',
                endpoint_url='http://localhost:8000',
                region_name="fake_region",
                aws_access_key_id="fake_id",
                aws_secret_access_key="fake_key")
    else:
        resource = boto3.resource('dynamodb',
                region_name='us-east-1',
                aws_access_key_id=os.environ['AWS_KEY'],
                aws_secret_access_key=os.environ['AWS_SECRET'])

    table = resource.Table('my_cookbook_users')
    key = {
        "userId": amazonId
    }
    updateExpr = 'SET bigoven_username=:b'
    exprAttributeValues = {':b': bigoven_username}
    condExpr = boto3.dynamodb.conditions.Attr('invocations').exists()
    try:
        response = table.update_item(Key=key,
                UpdateExpression=updateExpr,
                ExpressionAttributeValues=exprAttributeValues,
                ConditionExpression=condExpr)
    except ClientError as ce:
        print "invalid id: %s" % amazonId
        return render_template('error.html')

    return render_template('link.html')

if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(debug = True)
