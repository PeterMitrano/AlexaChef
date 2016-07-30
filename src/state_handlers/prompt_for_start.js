'use strict';

var Core = require('../core');
var Alexa = require('./alexa');

module.exports = Alexa.CreateStateHandler(Core.states.PROMPT_FOR_START, {
  'AMAZON.YesIntent': function() {
    this.handler.state = Core.states.NEW_RECIPE;
    this.emit(":ask", "What do you want to make? You can say something like, let's make steak, or how do I cook friend chicken.");
  },
  'AMAZON.NoIntent': function() {
    this.handler.state = Core.states.PROMPT_FOR_START;
    this.emit(":ask", "What can I help you with? Try asking to start a new recipe.");
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. I thought you wanted me to prompt you to start something new.");
  }
});

