from Response import Response

def lambda_handler(event, context):
    return Response().tell("hello world.");
