'use strict';

var Alexa = require('./alexa');
var Core = require('./core');

var AskTutorialHandlers = require('./ask_tutorial');
var AskSearchHandlers = require('./ask_search');
var IngredientsOrInstructionsHandler = require('./ingredients_or_instructions');
var NewRecipeHandlers = require('./new_recipe');
var PromptForStartHandlers = require('./prompt_for_start');
var TellTutorialHandlers = require('./tell_tutorial');

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

var StatelessHandlers = {
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
  'StartNewRecipeIntent': function () {
    this.emit("StartNewRecipeIntent" + Core.states.NEW_RECIPE);
  },
  'AMAZON.HelpIntent': function() {
    let ftu = Core.firstTimeIntroductionIfNeeded();
    if (!ftu) {
      this.emit(":tell", "If you need help, you can ask for the tutorial by saying, ask my .");
    }
  },
  'LaunchRequest': function () {
    let ftu = Core.firstTimeIntroductionIfNeeded();
    if (!ftu) {
      this.emit(":ask", "Hi again. Shall we make something?");
      this.handler.state = Core.states.ASK_MAKE_SOMETHING;
    }
  },
  'Unhandled': function() {
    let ftu = Core.firstTimeIntroductionIfNeeded();
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
