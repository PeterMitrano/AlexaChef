'use strict';

var states = {
    START: '_START',
    ONLINE_SEARCH:

};

var Alexa = require('alexa-sdk');

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

var handlers = {

  'StartNewRecipeIntent': function () {
    // javascript why do you suck so much?
    // check if the slot is empty *sigh*
    let recipe_name = this.event.request.intent.slots.RecipeName.value;
    if (this.event.request.intent.slots.RecipeName.value === undefined) {
      this.emit(":tell", 'I couldn\'t figure what recipe you wanted. Try saying, How do I make pancakes?',
        'Try saying, How do I make pancakes?');
    }
    else {
      // here we make an API call and find out if the user has a recipe for this already or not.
      let user_has_recipe = Math.random() < 0.5; // TODO: make api call, for now it's random
      if (user_has_recipe) {
        this.emit(":ask", 'I found a recipe for ' + recipe_name ', In your cookbook. Do you want to use that?');
      }
      else {
        this.emit(":ask", 'I didn\'t find any recipe for ' + recipe_name ', In your cookbook. Should I find one online?',
          'Do you want to find another recipe?');
      }
    }
  },
  'AMAZON.NextIntent': function() {
    this.emit("AMAZON.NextIntent");
  },
  'AMAZON.HelpIntent': function() {
    this.emit("AMAZON.HelpIntent");
  },
  'NewSession': function () {
    console.log("NewSession");
  },
  'OnSessionStarted': function () {
    console.log("OnSessionStarted");
  },
  'OnSessionEnded': function () {
    console.log("OnSessionEnded");
  },
  'OnLaunch': function () {
    console.log("OnLaunch");
  },
  'Unhandled': function() {
    console.log("Unhandled");
  }
};


/** the function that alexa will call when envoking our skill.
* The execute method essentially dispatches to on of our session handlers */
exports.handler = function(event, context) {
  var alexa = Alexa.handler(event, context);
  alexa.registerHandlers(handlers);
  alexa.APP_ID = APP_ID;
  alexa.execute();
};
