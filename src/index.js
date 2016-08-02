/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

'use strict';

var Alexa = require('./alexa');
var Core = require('./core');

var AskMakeCookbookHandlers = require('./state_handlers/ask_make_cookbook');
var AskSearchHandlers = require('./state_handlers/ask_search');
var AskTutorialHandlers = require('./state_handlers/ask_tutorial');
var IngredientsOrInstructionsHandler = require('./state_handlers/ingredients_or_instructions');
var InitialHandlers = require('./state_handlers/initial');
var NewRecipeHandlers = require('./state_handlers/new_recipe');
var PromptForStartHandlers = require('./state_handlers/prompt_for_start');
var TellTutorialHandlers = require('./state_handlers/tell_tutorial');

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

/**
 * Handle requests from the user when we are not in any given state.
 * This usually means the first time the user launches a new session,
 * but it could be other things
 */
var StatelessHandlers = {
  'NewSession': function () {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit("LaunchRequest" + Core.states.INITIAL_STATE);
  },
  'AMAZON.HelpIntent': function() {
    this.handler.state = Core.states.ASK_TUTORIAL;
    this.emit("AMAZON.YesIntent" + Core.states.ASK_TUTORIAL);
  },
  'AMAZON.StartOverIntent': function() {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit(":ask", "Alright, I've reset everything. I'm ready to start a new recipe.");
  },
  'SessionEndedRequest': function () {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit(":tell", "Goodbye.");
    this.emit(":saveState", true);
  },
  'Unhandled': function () {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit(":tell", `We've already been talking but I have no idea what about,
        so I will exit this session. Please start over by saying, Alexa launch my cookbok.`);
    this.emit(":saveState", true);
  }
};

/**
 * the function that alexa will call when envoking our skill.
 * The execute method essentially dispatches to on of our session handlers
 */
exports.handler = function(event, context, callback) {

  let params = {
    saveOnEndSession: false,
    endpoint_url: "http://localhost:8000"
  };

  var alexa = Alexa.LambdaHandler(event, context, callback, params);

  alexa.dynamoDBTableName = 'my_cookbook_users';
  alexa.appId = APP_ID;

  alexa.registerHandlers(StatelessHandlers,
    AskMakeCookbookHandlers,
    AskSearchHandlers,
    AskTutorialHandlers,
    IngredientsOrInstructionsHandler,
    InitialHandlers,
    TellTutorialHandlers,
    PromptForStartHandlers,
    NewRecipeHandlers
    );

  console.log("State: " + JSON.stringify(event.session.attributes, null, 2));

  alexa.execute();
};
