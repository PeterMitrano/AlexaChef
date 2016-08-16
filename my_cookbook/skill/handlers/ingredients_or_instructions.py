from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipe_reader


class IngredientsOrInstructionsHandler():
    def IngredientsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't list ingredients because you haven't picked a recipe.")

        return recipe_reader.ingredients(attributes)

    def InstructionsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't start instructions because you haven't picked a recipe.")

        step_number = attributes.get('step_number', 0)

        return recipe_reader.instruct(step_number, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused. Do you want to start with ingredients or instructions?",
                             "Say which one you want.", attributes)


handler = IngredientsOrInstructionsHandler()
state = core.States.INGREDIENTS_OR_INSTRUCTIONS
