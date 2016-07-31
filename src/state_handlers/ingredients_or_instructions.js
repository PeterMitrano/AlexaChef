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
    this.emit(":ask", "Starting with ingredients");
  },
  'InstructionsIntent': function() {
    this.emit(":ask", "Starting with instructions");
  },
  'Unhandled': function() {
    this.emit(":ask", "I'm confused. Do you want to start with ingredients or instructions?");
  }
});

