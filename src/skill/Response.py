import json

class Response:

  def __init__(self):
    self.body = {
      "version": "1.0",
      "sessionAttributes": {
      },
      "response": {
        "outputSpeech": {
          "type": "SSML",
          "ssml": ""
        },
      }
    }

  def ask(self, speech_output, reprompt_speech):
    pass

  def tell(self, speech_output):
    pass

  def ask_with_card(self, speech_output, reprompt_speech, card_title, card_content, card_img_url):
    pass

  def tell_with_card(self, speech_output, card_title, card_content, card_img_url):
    pass
