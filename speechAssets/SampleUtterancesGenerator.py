#!/usr/bin/python

import shutil
from os import path
from expand import expand

recipe_literals = [
    'meatloaf',
    'chicken with rice',
    'pizza',
    'chocolate chip cookies',
    'pumpkin muffins',
    'black bean burritos with peas',
    'Granola with Fresh Fruit',
    'Healthy Breakfast Frittata',
    'Healthy Lifestyle Tea',
    'Italian Tofu Frittata',
    'Perfect Oatmeal',
    'Poached Eggs over Spinach',
    'Quinoa Power Breakfast',
    'Swiss Breakfast',
    'Black Bean Salad',
    'Greek Garbanzo Bean Salad',
    'Halibut Salad',
    'Shrimp and Avocado Salad',
    'Turkey Chefs Salad',
    'Broiled Salmon Salad',
    'Dulse Cucumber Salad',
    'Garlic Shrimp Salad',
    'Greek Salad',
    'Ground Lamb Salad',
    'Healthy Chicken Caesar Salad',
    'Lentil Salad',
    'Marinated Bean Salad',
    'Mediterranean-Style Salad',
    'Soy Bean and Fennel Salad',
    'Tuna Salad Surprise',
    'Barley Mushroom Soup',
    'Red Kidney Bean Soup with Lime Yogurt',
    'Seafood Gazpacho',
    'Zesty Mexican Soup',
    'Baked Salmon and Walnut Patties With Red Bell Pepper Sauce',
    'Braised Cod with Celery',
    'Healthy Sauteed Seafood with Asparagus',
    'Quick Broiled Salmon with Ginger Mint Salsa',
    'Salmon in Citrus Sauce',
    'Roast Turkey Breast with Chipotle Chili Sauce',
    'Curried Mustard Greens and Garbanzo Beans with Sweet Potatoes',
    'Warm Quinoa Salad',
    'Cranberry Sauce',
    'Creamy Romaine Salad',
    'five Minute Green Beans',
    'five Minute Healthy Sauteed Cauliflower with Turmeric',
    'Mediterranean Pinto Beans',
    'Pinto Beans with Collard Greens',
    'ten Minute Fresh Berry Dessert with Yogurt and Chocolate',
    'ten Minute Kiwi Mandala',
    'Sesame Bar',
    'Perfect Oatmeal',
    'Poached Huevos Rancheros',
    'five Minute Miso Soup with Dulse',
    'Vegetarian Healthy Saute',
    'Asparagus Salad',
    'Great Antipasto Salad',
    'Kiwi Salad',
    'Side Vegetables',
    'Healthy Sauteed Shiitake Mushrooms',
    'Healthy Sauteed Onions',
    'Healthy Creamed Corn',
    'Healthy Mashed Sweet Potatoes',
    'Roasted Beets',
    'Sauteed Greens',
    'ten Minute Fresh Berry Dessert with Yogurt and Chocolate',
    'ten Minute Orange Treat',
    'ten Minute Peanut Bars',
    'five Minute Grapes in Honey-Lemon Sauce',
    'Apple Treats',
    'Blueberry Parfait',
    'Blueberry Trifle',
    'Cranberry and Fresh Pear Cobbler',
    'Fresh Peaches with Blueberries and Yogurt',
    'Ginger Yogurt with Fruit',
    'Grapefruit Sunrise',
    'No-Bake Apple Walnut Tart',
    'Papaya with Lime',
    'Tropical Banana Treat',
]

ways_to_cook = [
    'bake',
    'roast',
    'broil',
    'puree',
    'braise',
    'caramelize',
    'deep fry',
    'grill',
    'juice',
    'marinate',
    'pickle',
    'steam',
    'sear',
    'boil',
    'poach',
    'fry',
]

extensions = [
    {
        'intent': "No",
        'samples': [
            'No find me another one',
            'No not that one',
            'No not that',
            'No find something else',
        ]
    },
    {
        'intent': "Help",
        'samples': [
            'What can I say next',
        ]
    },
    {
        'intent': "Next",
        'samples': [
            'go on',
            'next step',
            'what\'s next',
        ]
    },
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
            [['Find me a recipe for', 'Let\'s make'], ' {', recipe_literals, '|RecipeName}'],
            [['How do I', 'Show me how to', 'Help me'], ' ',  words_for_cook, ' {', recipe_literals, '|RecipeName}'],
            [['show', 'tell'], ' me how to ' , words_for_cook,  ' {', recipe_literals, '|RecipeName}'],
            ['How is {', recipe_literals ,'|RecipeName} ' , words_for_cook],
        ]
    },
    {
        'name': 'IngredientsIntent',
        'samples': [
            ['Ingredients'],
            ['The ingredients'],
        ]
    },
    {
        'name': 'InstructionsIntent',
        'samples': [
            ['Instructions'],
            ['The instructions'],
        ]
    }

]


if __name__=="__main__":
    # backup a copy first
    if path.isfile('SampleUtterances.txt'):
        shutil.copy2('SampleUtterances.txt', 'SampleUtterances.txt.bak')

    f = open('SampleUtterances.txt','w')

    for extension in extensions:
        for sample in extension['samples']:
            f.write('AMAZON.' + extension['intent'] + 'Intent' + ' ' + sample + '\n')

    for intent in intents:
        for sample in intent['samples']:
            variants = expand(sample)
            for variant in variants:
                variant_str = "".join(variant)
                f.write(intent['name'] + ' ' + variant_str + '\n')

    f.close()

