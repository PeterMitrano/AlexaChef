from skill import Response

def lambda_handler(event, context):
  return Response.tell_with_card("hello world.", "title", "content", None);
