from my_cookbook.util import core
from my_cookbook.util import responder


class IngredientsOrInstructionsHandler():
    def IngredientsIntent(self, handlers, persistant_attributes, attributes, slots):
        # make request to my API
        return responder.tell_with_card("Here are the ingredients", "Ingredients",
                                        " - eggs\n - milk", None)

    def InstructionsIntent(self, handlers, persistant_attributes, attributes, slots):
        # make request to my API
        return responder.tell_with_card(
            "Here are the instructions", "Instructions",
            " - mix eggs and milk\n - throw it on the ground\n - profit", None)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        return responder.ask("I'm confused. Do you want to start with ingredients or instructions?",
                             "Say which one you want.", attributes)


handler = IngredientsOrInstructionsHandler()
state = core.States.INGREDIENTS_OR_INSTRUCTIONS
