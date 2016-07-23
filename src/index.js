var AlexaSkill = require("./AlexaSkill");

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

/**
 * Represents a the overall skill object.
 * @constructor
 */
var MyCookbook = function() {
  AlexaSkill.call(this, APP_ID);
};

MyCookbook.prototype =  Object.create(AlexaSkill.prototype);
MyCookbook.prototype.constructor = MyCookbook;


/** called when the user makes their first request per session.
 * Could be as simple as "Alexa, ask My Cookbook"
 * @param sessionStartedRequest the request body
 * @param session session object useful for tracking within a session
 */
MyCookbook.prototype.eventHandlers.onSessionStarted =
  function(sessionStartedRequest, session) {

  console.log("on Session Started. request id:" +
      sessionStartedRequest.requestId +
      " session id:" +
      session.sessionId);
};

/** called when the user invokes our skill with no intent.
 * IE "Alexa, ask my cookbook" */
MyCookbook.prototype.eventHandlers.onLaunch =
  function(launchRequest, session, response) {

  var output = "Hello, I'm your Cookbook." +
    " You can ask me how to make a recipe, and I will walk you through it. ";

  var reprompt = "Ask me how to make meatloaf.";

  response.ask(output, reprompt);

  console.log("onLaunch requestId: " +
      launchRequest.requestId +
      ", sessionId: " +
      session.sessionId);
};

/** called when the user launches with one of the specified intents **/
MyCookbook.prototype.intentHandlers = {

  NextClassIntent: function(intent, session, response) {
    response.tell("your next class is physics.");
  },

  ListClassesIntent: function(intent, session, response) {
    response.tell("your classes are physics 1001 and chemistry 1001");
  },

  AMAZONStartOverIntent: function(intent, session, response) {
    console.log("intent: AMAZONStartOverIntent");
    response.tell("ughhh this is going to take forever.");
  },

  AMAZONRepeatIntent: function(intent, session, response) {
    console.log("intent: AMAZONRepeatIntent");
    response.tell("I shouldn't have to repeat myself");
  },

  AMAZONHelpIntent: function(intent, session, response) {
    console.log("intent: AMAZONHelpIntent");
    response.tell("no help for you!");
  },

  AMAZONYesIntent: function(intent, session, response) {
    console.log("intent: AMAZONYesIntent");
  },

  AMAZONNoIntent: function(intent, session, response) {
    console.log("intent: AMAZONNoIntent");
  },

  AMAZONStopIntent: function(intent, session, response) {
    console.log("intent: AMAZONStopIntent");
  },

  AMAZONCancelInten: function(intent, session, response) {
    console.log("intent: AMAZONCancelInten");
  }
};

/** the function that alexa will call when envoking our skill.
* The execute method essentially dispatches to on of our session handlers */
exports.handler = function(event, context) {
  var skill = new MyCookbook();
  skill.execute(event, context);
};
