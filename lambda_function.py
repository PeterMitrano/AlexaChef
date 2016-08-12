from my_cookbook.skill import main

_skill = {}


def handle_event(event, context):
    global _skill
    _skill = main.Skill()
    return _skill.handle_event(event, context)
