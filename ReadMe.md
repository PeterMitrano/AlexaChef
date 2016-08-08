# My Cookbook
[![Master Build Status](https://travis-ci.org/PeterMitrano/my_cookbook.svg?branch=master)](https://travis-ci.org/PeterMitrano/my_cookbook)

#### An Alexa Skill to help out in the kitchen

## Development

This project uses the local dyanmodb jar which you can download from aws, as well as virtual env.

 - Download extract [the dynamodb tar file](http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz)
 - In that folder, run `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
 - run tests

    nosetest -v

or for no work-in-progress tests

    nosetest -v -a \!wip

or for only wip tests

    nosetest -v -a wip
