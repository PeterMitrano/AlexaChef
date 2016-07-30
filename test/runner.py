#!/usr/bin/python

# A test runner for my_cookbook built using boto3, the python
# sdk for aws services

import base64
import boto3
import json
import pprint
import re

def no_unicode(object, context, maxlevels, level):
    """ change unicode u'foo' to string 'foo' when pretty printing"""
    if pprint._type(object) is unicode:
        object = str(object)
    return pprint._safe_repr(object, context, maxlevels, level)

pp = pprint.PrettyPrinter(indent=2)
pp.format = no_unicode

class bcolors:
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

if __name__ == '__main__':
  lambda_client = boto3.client("lambda")

  payload_file = open('./test/payload.json', 'r')

  # > ./build/encoded_tail.json
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
    pp.pprint(result_json)
  else:
    print bcolors.BOLD + bcolors.YELLOW, 'No payload in response.', bcolors.ENDC
