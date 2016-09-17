import logging
import json

from my_cookbook.skill import main
from my_cookbook.util import core

_skill = None


def handle_event(event, context):
    logging.getLogger(core.LOGGER).warn(json.dumps(event, indent=2))

    global _skill
    _skill = main.Skill()
    return _skill.handle_event(event, context)
