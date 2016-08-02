'use strict';

let index = require("../src/index");
let generator = require("./generate_intents");

function callback(error, result) {
  if (error) {
    console.log("ERROR " + JSON.stringify(error, null, 2));
  }
  if (result) {
    console.log("RESULT " + JSON.stringify(result, null, 2));
  }
}

// this is literally never used
let context = {
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

console.log("REQUEST: " + JSON.stringify(event, null, 2));
index.handler(event, context, callback);
