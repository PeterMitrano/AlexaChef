from my_cookbook.util import responder
from my_cookbook.util import core

ingredient_pause_time = 1.3


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

def instructions_card(instructions):
    separator = '\n - '
    return separator.join(instructions)
