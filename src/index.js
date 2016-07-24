'use strict';

var Alexa = require('alexa-sdk');

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

var handlers = {

  'StartNewRecipeIntent': function () {
    console.log("StartNewRecipeIntent");
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
