# My Cookbook
[![Master Build Status](https://travis-ci.org/PeterMitrano/my_cookbook.svg?branch=master)](https://travis-ci.org/PeterMitrano/my_cookbook)

#### An Alexa Skill to help out in the kitchen

## Development

In the `src` directory:

Use `npm install` to get everything you need.
Run `grunt`. This will run jshint and generate jsdocs.

### Generating sample utterances

    cd test
    node generate_utterances.js


### Running local webserver & database for testing

 - Download extract (the dynamodb tar file)[http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz]
 - In that folder, run `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
 - Install Nodemon (such as with `npm install -g nodemon`
 - Go to the test folder of this project and run `nodemon server.js`
 - Open up a browser and point it to (http://localhost:4000)[http://localhost:4000]
