from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipe_reader


class IngredientsOrInstructionsHandler():
    def IngredientsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't list ingredients because you haven't picked a recipe.")

        speech = recipe_reader.ingredients_speech(attributes['current_recipe'])
        card = recipe_reader.ingredients_card(attributes['current_recipe'])
        return responder.ask_with_card("The ingredients are. " + speech + ". Do you want to hear \
                instructions, or ingredients again?", None, "Ingredients", card, None, attributes)

    def InstructionsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't start instructions because you haven't picked a recipe.")

        step_number = attributes.get('step_number', 0)

        instructions = attributes['current_recipe']['Instructions']
        if len(instructions) <= step_number:
            return responder.tell("this recipe doesn't have any instructions.")

        instruction = instructions[step_number]
        card = recipe_reader.instructions_card(attributes['current_recipe'])

        return responder.ask_with_card(
            instruction + ". <break time=2/> would you like to hear the next step?", None,
            "Instructions", card, None, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused. Do you want to start with ingredients or instructions?",
                             "Say which one you want.", attributes)


handler = IngredientsOrInstructionsHandler()
state = core.States.INGREDIENTS_OR_INSTRUCTIONS
