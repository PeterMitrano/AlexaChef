'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

module.exports = Alexa.CreateStateHandler(Core.states.PROMPT_FOR_START, {
  'AMAZON.YesIntent': function() {
    this.handler.state = Core.states.NEW_RECIPE;
    this.emit(":ask", "What do you want to make? You can say something like, let's make steak, or how do I cook fried chicken.");
  },
  'AMAZON.NoIntent': function() {
    this.handler.state = Core.states.PROMPT_FOR_START;
    this.emit(":ask", "What can I help you with? Try asking to start a new recipe.");
  },
  'StartNewRecipeIntent': function() {
    this.emit("StartNewRecipeIntent" + Core.states.NEW_RECIPE);
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. Try asking for start a new recipe, or ask to quit.");
  }
});

