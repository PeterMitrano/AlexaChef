/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

'use strict';

var Alexa = require('./alexa');
var Core = require('./core');

var AskTutorialHandlers = require('./state_handlers/ask_tutorial');
var AskSearchHandlers = require('./state_handlers/ask_search');
var IngredientsOrInstructionsHandler = require('./state_handlers/ingredients_or_instructions');
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
  /** Called any time the 'new' attribute is true and we're not in any specific state. */
  'NewSession': function () {
    let ftu = Core.firstTimeIntroductionIfNeeded(this);

    if (!ftu) {
      this.emit(":ask", "Welcome back! Tell me what you want to make.");
      this.handler.state = Core.states.NEW_RECIPE;
      this.attributes.invocations += 1;
    }

    // we always increment in this Intent, so we must save that
    console.log("invocations: " + this.attributes.invocations);
    this.emit(':saveState', true);
  },
  /** User can start off by immediately asking for a recipe */
  'StartNewRecipeIntent': function () {
    this.emit("StartNewRecipeIntent" + Core.states.NEW_RECIPE);
  },
  /** The user says something like "ask my cookbook for help" */
  'AMAZON.HelpIntent': function() {
    let ftu = Core.firstTimeIntroductionIfNeeded(this);
    if (!ftu) {
      this.emit(":tell", "If you need help, you can ask for the tutorial by saying, ask my .");
    }
  },
  /** The user says something like "Open my cookbook" */
  'LaunchRequest': function () {
    let ftu = Core.firstTimeIntroductionIfNeeded(this);
    if (!ftu) {
      this.emit(":ask", "Hi again. Shall we make something?");
      this.handler.state = Core.states.ASK_MAKE_SOMETHING;
    }
  },
  /** Any intents not handled above go here */
  'Unhandled': function() {
    let ftu = Core.firstTimeIntroductionIfNeeded(this);
    if (!ftu) {
      this.emit(":tell", "intent equals, Unhandled");
    }
  }
};

/** the function that alexa will call when envoking our skill.
* The execute method essentially dispatches to on of our session handlers */
exports.handler = function(event, context) {
  var alexa = Alexa.LambdaHandler(event, context);

  alexa.registerHandlers(StatelessHandlers,
    AskTutorialHandlers,
    AskSearchHandlers,
    IngredientsOrInstructionsHandler,
    TellTutorialHandlers,
    PromptForStartHandlers,
    NewRecipeHandlers
    );
  alexa.dynamoDBTableName = 'my_cookbook_users';
  alexa.appId = APP_ID;
  alexa.execute();
};
