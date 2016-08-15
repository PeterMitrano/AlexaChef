import logging

from my_cookbook.util import core
from my_cookbook.util import responder


class StatelessHandler():
    def SaveIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'current_recipe' in attributes:
            current_recipe = attributes['current_recipe']
            if 'recipes' in persistant_attributes:
                if current_recipe in persistant_attributes['recipes']:
                    attributes['tmp_state'] = attributes[core.STATE_KEY]
                    attributes[core.STATE_KEY] = core.States.CONFIRM_OVERWRITE_RECIPE
                    return responder.ask("This recipe is already in your cookbook. \
                            If you want to overwrite the existing recipe with this one, \
                            say yes. Say no to cancel and leave the existing recipe.",
                            "Do you want to overwrite with this recipe?",
                            attributes)
                else:
                    # it's new, so add it
                    persistant_attributes['recipes'].append(current_recipe)
            else:
                # recipe list doesn't exist
                persistant_attributes['recipes'] = [current_recipe]

        else:
            return responder.tell("I can't save a recipe because we're not working on one. \
                    Try searching for a recipe first")

    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.NEW_RECIPE], "StartNewRecipeIntent")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def AMAZON_HelpIntent(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.ASK_TUTORIAL], "AMAZON_YesIntent")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def AMAZON_StartOverIntent(self, handlers, persistant_attributes, attributes, slots):
        attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Alright, I've reset everything. I'm ready to start a new recipe.")

    def SessionEndedRequest(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        return responder.tell("Goodbye.")

    def LaunchRequest(self, handlers, persistant_attributes, attributes, slots):
        other_handler = getattr(handlers[core.States.INITIAL_STATE], "LaunchRequest")
        return other_handler(handlers, persistant_attributes, attributes, slots)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
        if attributes['new']:
            return responder.tell("We've already been talking" \
                " but I have no idea what about, so I will exit this session. Please" \
                " start over by saying, Alexa launch my cookbook.")
        else:
            return responder.tell("Hey, what's up.")


handler = StatelessHandler()
state = core.States.STATELESS
