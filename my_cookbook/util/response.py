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


def ask_with_card(speech_output, reprompt_speech, card_title, card_content,
                  card_img_url):
    response = {
        'outputSpeech': outputSpeech(speech_output),
        'reprompt': {
            'outputSpeech': outputSpeech(reprompt_speech)
        },
        'card': card(card_title, card_content, card_img_url),
        'shouldEndSession': False
    }
    return fini({}, response)


def tell_with_card(speech_output, card_title, card_content, card_img_url):
    response = {
        'outputSpeech': outputSpeech(speech_output),
        'card': card(card_title, card_content, card_img_url),
        'shouldEndSession': True
    }
    return fini({}, response)


def card(card_title, card_content, card_img_url):
    if card_img_url:
        return {
            'type': 'Standard',
            'title': card_title,
            'text': card_content,
            'image': {
                'smallImageUrl': card_img_url,
                'largeImageUrl': card_img_url
            }
        }
    else:
        return {'type': 'Simple', 'title': card_title, 'content': card_content}


def outputSpeech(ssml):
    return {"type": "SSML", "ssml": "<speak>" + ssml + "</speak>"}


def fini(attributes, response):
    return {
        "version": "1.0",
        "sessionAttributes": attributes,
        "response": response
    }
