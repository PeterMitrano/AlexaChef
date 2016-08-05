from skill import Response

def lambda_handler(event, context):
    return Response.tell("hello world.");
