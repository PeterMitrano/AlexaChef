'use strict';

let app = require("../src/index.js");

function callback(error, result) {
  if (error) {
    console.log("ERROR " + JSON.stringify(error, null, 2));
  }
  if (result) {
    //console.log("RESULT " + JSON.stringify(result, null, 2));
  }
}

// this is literally never used
let context = {
    "callbackWaitsForEmptyEventLoop": true,
    "logGroupName": "/aws/lambda/MyCookbook",
    "logStreamName": "2016/08/02/[$LATEST]d0d90c205b9b48a897302d551a1b44ef",
    "functionName": "MyCookbook",
    "memoryLimitInMB": "128",
    "functionVersion": "$LATEST",
    "invokeid": "4088ab1b-585d-11e6-b808-d577e18f6fe1",
    "awsRequestId": "4088ab1b-585d-11e6-b808-d577e18f6fe1",
    "invokedFunctionArn": "arn:aws:lambda:us-east-1:498480461879:function:MyCookbook"
}

let event = {
  "session": {
    "sessionId": "SessionId.1a537f57-a81a-4137-9668-081706165673",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05"
    },
    "attributes": {
    },
    "user": {
      "userId": "amzn1.account.AHI6EJHVJCBLLXLYYZLZHXEX2KNQ"
    },
    "new": true
  },
  "request": {
    "type": "LaunchRequest",
    "requestId": "EdwRequestId.061528dc-189c-4945-8b2e-64aa70fceaa5",
    "locale": "en-US",
    "timestamp": "2016-07-31T05:18:55Z",
    "intent": {
      "name": "AMAZON.YesIntent",
      "slots": {
        "RecipeName": {
          "name": "RecipeName"
        }
      }
    }
  },
  "version": "1.0"
}

//console.log("REQUEST: " + JSON.stringify(event, null, 2));
app.handler(event, context, callback);
