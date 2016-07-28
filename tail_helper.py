#!/usr/bin/python

import sys
import base64
import json

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

if __name__ == '__main__':
    if len(sys.argv) == 2:
        f = open(sys.argv[1], 'r')

        with open(sys.argv[1], 'r') as myfile:
            file_as_string = myfile.read().replace('\n', '')

            file_as_json = json.loads(file_as_string)
            status = file_as_json['StatusCode']

            if status != 200:
                print bcolors.RED, 'StatusCode:', status, bcolors.ENDC

            result = file_as_json['LogResult']
            human_readable_string = base64.b64decode(result)
            print bcolors.BOLD + bcolors.BLUE + "Console Output" + bcolors.ENDC
            print human_readable_string

    else:
        print "must pass argument name of tail file"
