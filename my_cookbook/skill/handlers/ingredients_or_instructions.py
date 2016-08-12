from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipe_reader


class IngredientsOrInstructionsHandler():
    def IngredientsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't list ingredients because you haven't picked a recipe.")

        # because it's a tell, we save attributes
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        persistant_attributes['current_recipe'] = attributes['current_recipe']

        ingredients_speech = recipe_reader.ingredients_speech(attributes[
            'current_recipe'])
        card = recipe_reader.ingredients_card(attributes['current_recipe'])
        return responder.tell_with_card("The ingredients are. " + ingredients_speech, "Ingredients",
                                        card, None)

    def InstructionsIntent(self, handlers, persistant_attributes, attributes, slots):
        # check we've got a working recipe at the moment
        if 'current_recipe' not in attributes:
            return responder.tell("I can't start instructions because you haven't picked a recipe.")

        # because it's a tell, we save attributes
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        persistant_attributes['current_recipe'] = attributes['current_recipe']

        instructions_speech = recipe_reader.instructions_speech(attributes[
            'current_recipe'])
        card = recipe_reader.instructions_card(attributes['current_recipe'])
        return responder.tell_with_card("The ingredients are. " + instructions_speech,
                                        "Instructions", card, None)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused. Do you want to start with ingredients or instructions?",
                             "Say which one you want.", attributes)


handler = IngredientsOrInstructionsHandler()
state = core.States.INGREDIENTS_OR_INSTRUCTIONS
