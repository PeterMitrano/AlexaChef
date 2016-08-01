'use strict';

var utterances = require("alexa-utterances");

let intents = [
  {
    "name": "StartNewRecipeIntent",
    "dictionary": {
      "a": ['Find me a recipe for', 'Let\s make'],
      "b": ['How do I', 'Show me how to', 'Help me'],
      "c": ['show', 'tell'],
      "words_for_cook": ['cook', 'make', 'create'],
      "recipes": [
          //'meatloaf',
          //'chicken with rice',
          //'pizza',
          //'chocolate chip cookies',
          //'pumpkin muffins',
          //'black bean burritos with peas',
          //'Granola with Fresh Fruit',
          //'Healthy Breakfast Frittata',
          //'Healthy Lifestyle Tea',
          //'Italian Tofu Frittata',
          //'Perfect Oatmeal',
          //'Poached Eggs over Spinach',
          //'Quinoa Power Breakfast',
          //'Swiss Breakfast',
          //'Black Bean Salad',
          //'Greek Garbanzo Bean Salad',
          //'Halibut Salad',
          //'Shrimp and Avocado Salad',
          //'Turkey Chefs Salad',
          //'Broiled Salmon Salad',
          //'Dulse Cucumber Salad',
          //'Garlic Shrimp Salad',
          //'Greek Salad',
          //'Ground Lamb Salad',
          //'Healthy Chicken Caesar Salad',
          //'Lentil Salad',
          //'Marinated Bean Salad',
          //'Mediterranean-Style Salad',
          //'Soy Bean and Fennel Salad',
          //'Tuna Salad Surprise',
          //'Barley Mushroom Soup',
          //'Red Kidney Bean Soup with Lime Yogurt',
          //'Seafood Gazpacho',
          //'Zesty Mexican Soup',
          //'Baked Salmon and Walnut Patties With Red Bell Pepper Sauce',
          //'Braised Cod with Celery',
          //'Healthy Sauteed Seafood with Asparagus',
          //'Quick Broiled Salmon with Ginger Mint Salsa',
          //'Salmon in Citrus Sauce',
          //'Roast Turkey Breast with Chipotle Chili Sauce',
          //'Curried Mustard Greens and Garbanzo Beans with Sweet Potatoes',
          //'Warm Quinoa Salad',
          //'Cranberry Sauce',
          //'Creamy Romaine Salad',
          //'five Minute Green Beans',
          //'five Minute Healthy Sauteed Cauliflower with Turmeric',
          //'Mediterranean Pinto Beans',
          //'Pinto Beans with Collard Greens',
          //'ten Minute Fresh Berry Dessert with Yogurt and Chocolate',
          //'ten Minute Kiwi Mandala',
          //'Sesame Bar',
          //'Perfect Oatmeal',
          //'Poached Huevos Rancheros',
          //'five Minute Miso Soup with Dulse',
          //'Vegetarian Healthy Saute',
          //'Asparagus Salad',
          //'Great Antipasto Salad',
          //'Kiwi Salad',
          //'Side Vegetables',
          //'Healthy Sauteed Shiitake Mushrooms',
          //'Healthy Sauteed Onions',
          //'Healthy Creamed Corn',
          //'Healthy Mashed Sweet Potatoes',
          //'Roasted Beets',
          //'Sauteed Greens',
          //'ten Minute Fresh Berry Dessert with Yogurt and Chocolate',
          //'ten Minute Orange Treat',
          //'ten Minute Peanut Bars',
          //'five Minute Grapes in Honey-Lemon Sauce',
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
  }
]

intents.forEach(function (intent) {
  intent.templates.forEach(function (template) {
    var result = utterances(template, intent.slots, intent.dictionary);
    console.log(result);
  });
});

