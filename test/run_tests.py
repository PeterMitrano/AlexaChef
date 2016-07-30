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


@click.command()
@click.option("--payload-filename", default="./test/Payload.json", help="file of json to send as request")
def run_tests(payload_filename):
    lambda_client = boto3.client("lambda")

    payload_file = open(payload_filename, 'r')

    response = lambda_client.invoke(FunctionName = 'MyCookbook', InvocationType = 'RequestResponse', LogType = 'Tail', Payload= payload_file)

    if response['StatusCode'] != 200:
        print bcolors.BOLD + bcolors.RED, 'Failure!', bcolors.ENDC, response['StatusCode']
    else:
        print bcolors.BOLD + bcolors.GREEN, 'Response OK!', bcolors.ENDC

    if 'FunctionError' in response:
        print bcolors.BOLD + bcolors.RED, 'Function Error:', bcolors.ENDC
        print response['FunctionError']

    if response['LogResult']:
        print bcolors.BOLD + bcolors.BLUE, 'Log Result:', bcolors.ENDC
        human_readable_string = base64.b64decode(response['LogResult'])
        lines = human_readable_string.rsplit('\n')
    for line in lines:
        if not re.match('.*RequestId.*', line):
            print line

    if 'Payload' in response:
        result = response['Payload']
        print bcolors.BOLD + bcolors.GREEN, 'Response:', bcolors.ENDC
        result_str = result.read()
        result_json = json.loads(result_str);
        print(json.dumps(result_json, indent=4))
    else:
        print bcolors.BOLD + bcolors.YELLOW, 'No payload in response.', bcolors.ENDC

if __name__ == "__main__":
    run_tests()
