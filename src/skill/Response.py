from copy import deepcopy
import json

default_body = {
  "version": "1.0",
  "sessionAttributes": {
  },
  "response": {
  }
}


def ask(speech_output, reprompt_speech):
  response = {
    'outputSpeech': outputSpeech(speech_output),
    'reprompt': {
      'outputSpeech': outputSpeech(reprompt_speech)
    },
    'shouldEndSession': False
  }
  return fini({}, response)

def tell(speech_output):
  response = {
    'outputSpeech': outputSpeech(speech_output),
    'shouldEndSession': True
  }
  return fini({}, response)

def ask_with_card(speech_output, reprompt_speech, card_title, card_content, card_img_url):
  pass

def tell_with_card(speech_output, card_title, card_content, card_img_url):
  pass

def outputSpeech(ssml):
  return {
    "type": "SSML",
    "ssml": ssml
  }

def fini(attributes, response):
  return {
    "version": "1.0",
    "sessionAttributes": attributes,
    "response": response
  }
