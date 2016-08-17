import os

APP_ID = "amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05"
STATE_KEY = "STATE"
DB_TABLE = 'my_cookbook_users'
LOGGER = 'my_cookbook'
LOCAL_DB_URI = 'http://localhost:8000'


class States:
    ASK_MAKE_COOKBOOK = '_ASK_MAKE_COOKBOOK'
    ASK_MAKE_ONLINE = '_ASK_MAKE_ONLINE'
    ASK_FAVORITE = '_ASK_FAVORITE'
    ASK_SEARCH = '_ASK_SEARCH'
    ASK_TUTORIAL = '_ASK_TUTORIAL'
    ASK_MAKE_SOMETHING = '_ASK_MAKE_SOMETHING'
    ASK_WHICH_RECIPE = '_ASK_WHICH_RECIPE'
    CONFIRM_OVERWRITE_RECIPE = '_CONFIRM_OVERWRITE_RECIPE'
    INGREDIENTS_OR_INSTRUCTIONS = '_INGREDIENTS_OR_INSTRUCTIONS'
    INITIAL_STATE = '_INITIAL_STATE'
    NEW_RECIPE = '_NEW_RECIPE'
    PROMPT_FOR_START = '_PROMPT_FOR_START'
    SEARCH_ONLINE = '_SEARCH_ONLINE'
    STATELESS = ''
    TELL_TUTORIAL = '_TELL_TUTORIAL'


def all_states():
    states = []
    for var in vars(States):
        if not var.startswith('_'):
            states.append(getattr(States, var))
    return states


def load_key():
    try:
        return os.environ['BIG_OVEN_API_KEY']
    except KeyError as e:
        raise RuntimeError("bigoven api key not found: %s" % e.message)
