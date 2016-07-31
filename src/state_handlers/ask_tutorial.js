/**
 * @fileOverview
 * @author Peter Mitrano- mitranopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * Represents the reponses when we've just asked if the user wants to follow
 * a tutorial on how to use the app.
 */
module.exports = Alexa.CreateStateHandler(Core.states.ASK_TUTORIAL, {
  'AMAZON.YesIntent': function() {
    // for now we just shortcut and end here
    //
    // this.handler.state = Core.states.TELL_TUTORIAL;
    //
    this.emit(":tell", "I am capable of finding recipes and walking you through making them");
    this.emit(':saveState', false);
  },
  'AMAZON.NoIntent': function() {
    this.handler.state = Core.states.PROMPT_FOR_START;
    this.emit(":ask", "Are you ready to start making something? You can say yes, or ask me someting else.");
  },
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. Do you want to start with a tutorial? Try saying yes or no.");
  }
});

