from my_cookbook.util import responder
from my_cookbook.util import core

ingredient_pause_time = 1.3


def ingredients(attributes):
    speech = ingredients_speech(attributes['current_recipe'])
    card = ingredients_card(attributes['current_recipe'])
    return responder.ask_with_card("The ingredients are. " + speech, None, "Ingredients", card,
                                   None, attributes)

def ingredients_speech(recipe):
    """ return ingredients ready for speech

    uses custom break to seperate each ingredient """

    ingredients = [i['Name'] for i in recipe['Ingredients']]
    separator = '<break time="%ss"/>' % ingredient_pause_time
    return separator.join(ingredients)

def ingredients_card(recipe):
    ingredients = [i['Name'] for i in recipe['Ingredients']]
    separator = '\n - '
    return separator.join(ingredients)

def instruct(step_number, attributes):
    instructions = attributes['current_recipe']['Instructions']
    if len(instructions) <= step_number:
        return responder.tell("this recipe doesn't have any instructions.")

    instruction = instructions[step_number]
    card = instructions_card(attributes['current_recipe'])

    return responder.ask_with_card(
        instruction + ". <break time=2/> would you like to hear the next step?", None,
        "Instructions", card, None, attributes)

def instructions_card(instructions):
    separator = '\n - '
    return separator.join(instructions)
