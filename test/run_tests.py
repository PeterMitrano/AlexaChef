#!/usr/bin/python

# A test runner for my_cookbook built using boto3, the python
# sdk for aws services

import base64
import boto3
import click
import json
import re
import sys

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@click.group()
def cli():
  pass

@cli.command()
@click.option("-v", "--verbose", count=True)
@click.option('-q', "--quiet", is_flag=True)
@click.option("--payload-filename")
@click.option("--new/--not-new", default=True)
@click.option("--userid")
@click.option("--request", type=click.Choice(['launch', 'yes']))
def run_tests(verbose, quiet, payload_filename, new, userid, request):
    lambda_client = boto3.client("lambda")

    payload = None
    if payload_filename:
        payload = open(payload_filename, 'r')
        if verbose >= 1 and not quiet:
            print bcolors.BOLD, 'Using ', payload_filename, 'as request', bcolors.ENDC
    elif new and userid and request:
        payload = {
            "session": {
                "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05"
                },
                "attributes": {},
                "new": new,
                "user": {
                    "userId": userid
                }
            }
        }

        if request == 'launch':
            payload['request'] = {
                "type": "LaunchRequest"
            }
        elif request == 'yes':
            payload['request'] = {
                "type": "IntentRequest",
                "intent": {
                    "name": "AMAZON.YesIntent"
                }
            }
        else:
            if not quiet:
                print "Bad request type"
                return

        # convert from python dict to string for sending
        payload = json.dumps(payload)

        if verbose >= 1 and not quiet:
            print bcolors.BOLD, 'Request', bcolors.ENDC
            print payload
    else:
        if not quiet:
            print "Bad arguments"
        return

    # at this point paylod is either a json formatted string or a file object with the json in the file

    response = lambda_client.invoke(FunctionName = 'MyCookbook', InvocationType = 'RequestResponse', LogType = 'Tail', Payload = payload)

    if response['StatusCode'] != 200:
        if not quiet:
            print bcolors.BOLD + bcolors.RED, 'Failure!', bcolors.ENDC, response['StatusCode']
    else:
        if verbose >= 1 and not quiet:
            print bcolors.BOLD + bcolors.GREEN, 'Response OK!', bcolors.ENDC

    if 'FunctionError' in response:
        if not quiet:
            print bcolors.BOLD + bcolors.RED, 'Function Error:', bcolors.ENDC
            print response['FunctionError']

    if response['LogResult']:
        if verbose >= 1 and not quiet:
            print bcolors.BOLD + bcolors.BLUE, 'Log Result:', bcolors.ENDC
            human_readable_string = base64.b64decode(response['LogResult'])
            lines = human_readable_string.rsplit('\n')
            for line in lines:
                if not re.match('.*RequestId.*', line):
                    print line

    if 'Payload' in response:
        if not quiet:
            result = response['Payload']
            print bcolors.BOLD + bcolors.GREEN, 'Response:', bcolors.ENDC
            result_str = result.read()
            result_json = json.loads(result_str)
            print(json.dumps(result_json, indent=4))
    else:
        if not quiet:
            print bcolors.BOLD + bcolors.YELLOW, 'No payload in response.', bcolors.ENDC

@cli.command()
@click.option("--userid", default="user0", help="delete this user from the my_cookbook_users table")
def delete_user(userid):
    print "Are you sure you want to delete user", userid, "? [y/N]"
    answer = raw_input()
    if answer == "y" or answer == "Y":
        print "deleting", userid
        dynamo_client = boto3.client('dynamodb')
        key = {"userId": {"S" : userid}}
        dynamo_client.delete_item(TableName="my_cookbook_users", Key=key)
    else:
        print "Aborting."

if __name__ == "__main__":
    cli()
