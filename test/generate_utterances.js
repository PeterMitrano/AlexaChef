'use strict';

var utterances = require("alexa-utterances");

let the_intents = [
  {
    "name": "StartNewRecipeIntent",
    "dictionary": {
      "a": ['Find me a recipe for', 'Let\s make'],
      "b": ['How do I', 'Show me how to', 'Help me'],
      "c": ['show', 'tell'],
      "words_for_cook": ['cook', 'make', 'create'],
      "recipes": [
          'Bacon wrapped Beef Tenderloin Steaks with Smoked Paprika Butter',
          'Bacon Tomato and Blue Cheese Focaccia Sandwich',
          'Bacon and Cheese Quiche',
          'Biscuits with Sausage Gravy',
          'Blue Cheese Stuffed Hamburgers',
          'B.L.A.T. Sandwich with Spicy Chipotle Mayonnaise',
          'Butternut Squash Hash with Mexican Chorizo and Eggs',
          'Cheddar Chive and Sour Cream Omelette',
          'Creamy Cauliflower Soup with Bacon Cheddar and Chives',
          'Crustless Quiche with Ham Asparagus and Gruyere',
          'Curried Chicken Salad',
          'Curried Turkey Salad with Apples Cranberries and Walnuts',
          'Easy Egg Salad',
          'Egg in a Nest',
          'Farfalle with Pistachio Cream Sauce',
          'Grilled Chicken and Pineapple Pizza',
          'Grilled Rib Eye with Havarti Horseradish Fondue',
          'Hearty Spinach and Sausage Soup',
          'Herbed Tuna Salad with Feta and Pine Nuts',
          'Homemade Sloppy Joes',
          'Horseradish Meatloaf',
          'Macaroni and Cheese with Bacon Leeks and Thyme',
          'Monster Meatball Sandwiches',
          'Pasta with Tomato-Cream Sauce and Fresh Basil',
          'Roasted Chicken Thighs and Cauliflower',
          'Simple Carne Asada',
          'Smoky Spiced Black-Eyed Peas with Bacon',
          'Southwestern Macaroni Casserole',
          'Spice Rubbed Flank Steak',
          'Spiced Turkey Burgers with Green Olives and Feta',
          'Spiked Egg Nog French Toast',
          'The Ultimate Manwich',
          'Three Bean Vegetarian Chili',
          'Tomato Paella with Chorizo',
          'Tofu in Coconut Sauce with Ginger and Lemongrass',
          'Tuna Noodle Casserole',
          'Tuscan Chicken Under a Brick',
          'Veggie Chili Beans and Rice',
          'Whole Wheat Pasta with Browned Butter and Mizithra Cheese',
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
          'Garlic Shrimp Salad',
          'Greek Salad',
          'Ground Lamb Salad',
          'Healthy Chicken Caesar Salad',
          'Pork Loaf',
          'Burritos',
          'Tacos',
          'Pizza',
          'Egg salad sandwhich',
          'BLT',
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
          'Chicken with rice',
          'Tropical Banana Treat',
      ]
    },
    "slots" : {"RecipeName": 'LITERAL'},
    "templates": [
      '{a} {recipes|RecipeName}',
      '{b} {words_for_cook} {recipes|RecipeName}',
      '{c} me how to {words_for_cook} {recipes|RecipeName}',
      'How is {recipes|RecipeName} {words_for_cook}'
    ]
  },
  {
    "name": "InstructionsIntent",
    "templates": [
      'Instructions',
      'The ingredients',
      'Instructions please',
      'Instructions first',
    ]
  },
  {
    "name": "IngredientsIntent",
    "templates": [
      'Ingredients',
      'The ingredients',
      'Ingredients please',
      'Ingredients first',
    ]
  },
  {
    "name": "AMAZON.NoIntent",
    "templates": [
      'find me another one',
      'not that one',
      'not that',
      'No find something else',
    ]
  },
  {
    "name": "AMAZON.YesIntent",
    "dictionary": {
      "good_words": ['good', 'great', 'awesome', 'excellent'],
    },
    "templates": [
      'yes use that',
      'yes that one',
      'yes that',
      'yes that is {good_words}',
    ]
  },
  {
    "name": "AMAZON.StartOverIntent",
    "templates": []
  },
  {
    "name": "AMAZON.HelpIntent",
    "templates": [
      'What can I say next',
    ]
  },
  {
    "name": "AMAZON.NextIntent",
    "templates": [
      'go on',
      'next step',
      'what\'s next',
    ]
  }
];

function getIntents() {
  let result = {};
  the_intents.forEach(function (intent) {
    result[intent.name] = {
      "name": intent.name,
      "schema": {
        "slots": intent.slots,
        "utterances": "utterances"
      }
    };
  });
  return  result;
}

function getSchema() {
  let result = [];
  the_intents.forEach(function (intent) {
    let slots = []
    if (intent.slots) {
      Object.keys(intent.slots).forEach(function (key) {
        slots.push({"name": key, "type": intent.slots[key]});
      });
    }

    let x = {
      "intent": intent.name,
      "slots": slots
    };
    result.push(x);
  });
  return  {"intents": result}
}

function generateUtterances() {
  let result = "";
  the_intents.forEach(function (intent) {
    intent.templates.forEach(function (template) {
      let samples = utterances(template, intent.slots, intent.dictionary, true);
      samples.forEach(function (utterance) {
        result += intent.name + "\t" + utterance + "\n";
      });
    });
  });
  return result;
};

module.exports.generate = generateUtterances;
module.exports.schema = getSchema;
module.exports.intents = getIntents;

if (!module.parent) {
  console.log(generateUtterances());
}
