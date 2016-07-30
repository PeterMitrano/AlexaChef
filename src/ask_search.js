
'use strict';

var Core = require('./core');
var Alexa = require('./alexa');

module.exports = Alexa.CreateStateHandler(Core.states.ASK_SEARCH, {
  'AMAZON.YesIntent': function() {
    this.handers.state = Core.states.INGREDIENT_OR_INSTRUCTIONS;
    this.emit(":tell", "Which do you want to start with, the ingredients or the instructions?");
  },
  'AMAZON.NoIntent': function() {
    this.emit(":ask", "Ok, then what can I do for you?");

    // not sure what to do here. I want to remote any notion of state and start over
    delete this.handler.state;
    this.emit(':saveState', true);
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. Do you want to search online for your recipe? Try saying yes or no.");
  }
});
