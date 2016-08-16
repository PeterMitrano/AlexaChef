from my_cookbook.util import core
from my_cookbook.util import responder


class ConfirmOverwriteRecipe():
    def AMAZON_YesIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'current_recipe' not in attributes or 'tmp_state' not in attributes:
            return responder.tell(
                "Sorry, but I've forgotten which recipe you wanted to save. You'll have to start over.")

        current_recipe = attributes['current_recipe']
        persistant_attributes[core.STATE_KEY] = attributes['tmp_state']
        persistant_attributes['recipes'].append(current_recipe)
        return responder.tell('Recipe overwritten')

    def AMAZON_NoIntent(self, handlers, persistant_attributes, attributes, slots):
        #TODO: consider how we might recover/fail if this isn't the case
        if 'tmp_state' in attributes:
            persistant_attributes[core.STATE_KEY] = attributes['tmp_state']

        return responder.tell('Cancelling overwrite')

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        return responder.ask("I'm not sure what you mean. \
                Do you want to overwrite the existing recipe? Say yes or no", None, attributes)


handler = ConfirmOverwriteRecipe()
state = core.States.CONFIRM_OVERWRITE_RECIPE
