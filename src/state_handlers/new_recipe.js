/**
 * @fileOverview
 * @author Peter Mitrano- mitranopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * Represents the reponses when we expect the user to request to make a new recipe
 */
module.exports = Alexa.CreateStateHandler(Core.states.NEW_RECIPE, {
  'StartNewRecipeIntent': function () {
    // javascript why do you suck so much?
    // check if the slot is empty *sigh*
    let recipe_name = this.event.request.intent.slots.RecipeName.value;
    if (this.event.request.intent.slots.RecipeName.value === undefined) {
      this.emit(":tell", 'I couldn\'t figure what recipe you wanted. Try saying, How do I make pancakes?',
        'Try saying, How do I make pancakes?');
    }
    else {
      // here we make an API call and find out if the user has a recipe for this already or not.
      let user_has_recipe = Math.random() < 0.5; // TODO: make api call, for now it's random
      if (user_has_recipe) {
        this.handler.state = Core.states.ASK_MAKE_COOKBOOK;
        this.emit(":ask", 'I found a recipe for ' + recipe_name + ', In your cookbook. Do you want to use that?');
      }
      else {
        this.handler.state = Core.states.ASK_SEARCH;
        this.emit(":ask", 'I didn\'t find any recipe for ' + recipe_name + ', In your cookbook. Should I find one online?',
          'Do you want to find another recipe?');
      }
    }
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. Try telling me what you want to make.");
  }
});
