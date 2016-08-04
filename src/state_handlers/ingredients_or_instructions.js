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
    this.emit(":tellWithCard", "Here are the ingredients", "Ingredients", " - eggs\n - milk\n");
  },
  'InstructionsIntent': function() {
    this.emit(":tellWithCard", "Here are the instructions", "Instrcutions", " - mix eggs and milk\n - throw it on the ground\n -profit");
  },
  'Unhandled': function() {
    this.emit(":ask", "I'm confused. Do you want to start with ingredients or instructions?");
  }
});

