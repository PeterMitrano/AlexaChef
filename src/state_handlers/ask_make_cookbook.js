/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * Represents the reponses when we expect the user to request to make a new recipe
 */
module.exports = Alexa.CreateStateHandler(Core.states.ASK_MAKE_COOKBOOK, {
  'AMAZON.YesIntent': function () {
    this.handler.state = Core.states.INGREDIENTS_OR_INSTRUCTIONS;
    this.emit(":ask", "Do you want to start with the ingredients or the instructions?");
  },
  'AMAZON.NoIntent': function () {
    // return to initial state!
    this.handler.state = Core.states.ASK_SEARCH;
    this.emit(":ask", "I could search for one online?");
  },
  'Unhandled': function () {
    this.emit(":ask", "I'm confused. Do you want to make the recipe from your cookbook?");
  }
});
