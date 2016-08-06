/**
 * @fileOverview
 * @author Peter Mitrano- mitranopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * Represents the reponses when we've just asked if the user wants to hear the
 * instructions or the ingredients for a recipe
 */
module.exports = Alexa.CreateStateHandler(Core.states.INGREDIENTS_OR_INSTRUCTIONS, {
  'IngredientsIntent': function() {
    Core.makeRequest(Core.endpoints.recipe, function(err, response, body) {
     console.log("bloody hell mate");
     if (!err && response.statusCode == 200) {
        this.emit(":tellWithCard", "Here are the ingredients", "Ingredients", " - eggs\n - milk\n");
      }
      else {
        this.emit(":tell", "Sorry, I couldn't load the recipe. Try again later, or try another recipe");
      }
    });
  },
  'InstructionsIntent': function() {
    Core.makeRequest(Core.endpoints.recipe, function(err, response, body) {
     console.log("bloody hell mate");
     if (!err && response.statusCode == 200) {
        this.emit(":tellWithCard", "Here are the instructions", "Instructions",
            " - mix eggs and milk\n - throw it on the ground\n -profit");
      }
      else {
        this.emit(":tell", "Sorry, I couldn't load the recipe. Try again later, or try another recipe");
      }
    });
  },
  'Unhandled': function() {
    this.emit(":ask", "I'm confused. Do you want to start with ingredients or instructions?");
  }
});

