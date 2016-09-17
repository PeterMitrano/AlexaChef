import logging

from my_cookbook.util import core
from my_cookbook.util import responder
from my_cookbook.util import recipes_helper
from my_cookbook import stage


class NewRecipeHandler():
    def start_recipe_search(self, recipe_name, username, attributes):
        # search the users recipes to find appropriate recipes.
        # the value here is a (possibly empty) list of recipes in order
        # of some ranking I have yet to devise.
        recipes = recipes_helper.search_my_recipes(recipe_name, username)

        # TODO: here would be a good spot to ask questions to narrow down
        # which recipe the user wants to make. for now just pick the first one.
        if len(recipes) == 0:
            attributes[core.STATE_KEY] = core.States.ASK_SEARCH
            attributes['current_recipe_name'] = recipe_name
            return responder.ask("I didn't find any recipe for " + recipe_name +
                                 ", In your cookbook. Should I find one online?",
                                 "Do you want to find another recipe?", attributes)
        else:
            attributes[core.STATE_KEY] = core.States.ASK_MAKE_COOKBOOK
            best_guess_recipe_name = recipes[0]['Title']
            attributes['current_recipe'] = recipes[0]
            return responder.ask("I found a recipe for " + best_guess_recipe_name +
                                 ", In your cookbook. Do you want to use that?", None, attributes)

    def StartNewRecipeIntent(self, handlers, persistant_attributes, attributes, slots):
        if 'RecipeName' not in slots or 'value' not in slots['RecipeName']:
            attributes['asking_recipe_name'] = True
            attributes[core.STATE_KEY] = core.States.NEW_RECIPE
            return responder.ask("Sorry, what's the recipe?", None, attributes)
        else:
            username = persistant_attributes.get('bigoven_username', None)

            if not username:
                # set url for linking accounts--not very secure.
                if stage.PROD:
                    link_url = 'https://petermitrano.pythonanywhere.com/'
                else:
                    link_url = 'http://localhost:5000/'
                # user has to start over here, sorry.
                persistant_attributes[core.STATE_KEY] = core.States.INITIAL_STATE
                return responder.tell_with_card("I was unable to find your bigoven username. \
                        Use the link I sent you to connect your bigoven account.",
                                                "Link BigOven Account", "%s?amazonId=%s" %
                                                (link_url, attributes['user']), None)

            recipe_name = slots['RecipeName']['value']

            return self.start_recipe_search(recipe_name, username, attributes)

    def Unhandled(self, handlers, persistant_attributes, attributes, slots):
        asking_recipe = attributes.get('asking_recipe_name', False)

        if asking_recipe:
            logging.getLogger(core.LOGGER).warn("asking recipe:")
            logging.getLogger(core.LOGGER).warn(attributes)
            logging.getLogger(core.LOGGER).warn(slots)

        # presist current state and end interaction
        persistant_attributes[core.STATE_KEY] = attributes[core.STATE_KEY]
        return responder.tell("I'm confused. Try asking me what you want to make.")


handler = NewRecipeHandler()
state = core.States.NEW_RECIPE
