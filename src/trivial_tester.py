import json
from lambda_function import lambda_handler

event = {
  "session": {
    "sessionId": "SessionId.7e080ead-ae56-4cdf-8ee8-56fcd79ea2f8",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.account.AHI6EJHVJCBLLXLYYZLZHXEX2KNQ"
    },
    "new": True
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.4fd3dedd-2336-4cd8-9b54-4952fce6e810",
    "locale": "en-US",
    "timestamp": "2016-08-05T07:31:36Z",
    "intent": {
      "name": "IngredientsIntent",
      "slots": {}
    }
  },
  "version": "1.0"
}

json = json.dumps(lambda_handler(event, {}), indent=2, sort_keys=True)
print json
