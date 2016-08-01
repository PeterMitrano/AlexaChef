/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');
var attributesHelper = require('../DynamoAttributesHelper');

/**
 * Represents the reponses when we aren't really in any particular state.
 * This is also the state we should begin in for every new session
 */
module.exports = Alexa.CreateStateHandler(Core.states.INITIAL_STATE, {
  /** User can start off by immediately asking for a recipe */
  'StartNewRecipeIntent': function () {
    this.emit("StartNewRecipeIntent" + Core.states.NEW_RECIPE);
  },
  /** The user says something like "Open my cookbook" */
  'LaunchRequest': function () {
    let ftu = Core.firstTimeIntroductionIfNeeded(this);
    if (!ftu) {
      if (this.event.session.new) {
        this.attributes.invocations += 1;
        this.handler.state = Core.states.NEW_RECIPE;
        this.emit(":ask", "Hi again. What do you want to make?");
        this.emit(':saveState', true);
        return true;
      }
      else {
        this.emit(":tell", "I've already been launched");
      }
    }
  },
  'SessionEndedRequest': function() {
    this.emit(":tell", "Goodbye!");
  },
  /** Any intents not handled above go here */
  'Unhandled': function() {
    if (this.event.session.new) {
      let ftu = Core.firstTimeIntroductionIfNeeded(this);
      if (!ftu) {
        this.emit(":tell", "I'm not sure what you want. Try asking to make something.");
      }
    }
    else {
      this.emit(":tell", "I'm not sure what you want. start by asking to make something.");
    }
  }
});

