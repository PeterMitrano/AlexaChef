/**
 * @fileOverview
 * @author Peter Mitrano- mitranopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * Represents the reponses when we've just asked if the user wants to search
 * online for their recipe
 */
module.exports = Alexa.CreateStateHandler(Core.states.ASK_SEARCH, {
  'AMAZON.YesIntent': function() {
    this.handers.state = Core.states.INGREDIENTS_OR_INSTRUCTIONS;
    this.emit(":tell", "Which do you want to start with, the ingredients or the instructions?");
  },
  'AMAZON.NoIntent': function() {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit(":ask", "Ok, then what can I do for you?");
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. Do you want to search online for your recipe? Try saying yes or no.");
  }
});
