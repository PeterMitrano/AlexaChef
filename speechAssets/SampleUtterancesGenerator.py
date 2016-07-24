#!/usr/bin/python

import shutil
from os import path
from expand import expand

recipe_literals = [
    'meatloaf',
    'chicken with rice',
    'pizza',
    'roasted duck with a side of carrots',
    'chocolate chip cookies',
    'pumpkin muffins',
    'black bean burritos with peas',
]

ways_to_cook = [
    'bake',
    'roast',
    'broil',
    'puree',
    'sear',
    'boil',
    'poach',
    'fry',
]

words_for_cook = [
    'cook',
    'make',
    'create',
]

intents = [
    {
        'name': 'StartNewRecipeIntent',
        'samples': [
            [['Find me a recipe for', 'Let\'s make'], '{', recipe_literals, '|RecipeName}'],
            [['How do I', 'Show me how to', 'Help me'],  words_for_cook, '{', recipe_literals, '|RecipeName}'],
            [['show', 'tell'], 'me how to', words_for_cook, '{', recipe_literals, '|RecipeName}'],
            ['How is {', recipe_literals ,'|RecipeName}' , words_for_cook],
        ]
    }
]


if __name__=="__main__":
    # backup a copy first
    if path.isfile('SampleUtterances.txt'):
        shutil.copy2('SampleUtterances.txt', 'SampleUtterances.txt.bak')

    f = open('SampleUtterances.txt','w')

    for intent in intents:
        for sample in intent['samples']:
            variants = expand(sample)
            for variant in variants:
                variant_str = " ".join(variant)
                f.write(intent['name'] + ' ' + variant_str + '\n')

    f.close()

