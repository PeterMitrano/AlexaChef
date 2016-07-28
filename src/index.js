'use strict';

var Alexa = require('./alexa');

var states = {
    TUTORIAL: '_TUTORIAL',
    SEARCH_ONLINE: '_SEARCH_ONLINE',
    INGREDIENT_OR_INSTRUCTIONS: 'INGREDIENT_OR_INSTRUCTIONS',
};

/** this can be found on the amazon developer page for the skill */
var APP_ID = 'amzn1.echo-sdk-ams.app.5e07c5c2-fba7-46f7-9c5e-2353cec8cb05';

var handlers = {
  // A new session is called every time the user starts a new invocation
  // by addressing our skill
  'NewSession': function () {
    // first we want to see if this is the users first time ever
    if (this.attributes.invocations === undefined ||
        this.attributes.invocations === 0) {
      this.emit(":tell", "This is your first time using this skill.");
      console.log(this.attributes);
      this.attributes.invocations = 1;
    }
    else {
      this.emit(":tell", "Welcome back!");
      this.attributes.invocations += 1;
    }

    // force save number_of_invocations
    this.emit(':saveState', true);
  },

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
        this.emit(":ask", 'I found a recipe for ' + recipe_name + ', In your cookbook. Do you want to use that?');
      }
      else {
        this.emit(":ask", 'I didn\'t find any recipe for ' + recipe_name + ', In your cookbook. Should I find one online?',
          'Do you want to find another recipe?');
      }
    }
  },
  'AMAZON.NextIntent': function() {
    this.emit(":tell", "intent equals, AMAZON.NextIntent");
  },
  'AMAZON.HelpIntent': function() {
    this.emit(":tell", "intent equals, AMAZON.HelpIntent");
  },
  'OnSessionStarted': function () {
    this.emit(":tell", "intent equals, OnSessionStarted");
  },
  'OnSessionEnded': function () {
    this.emit(":tell", "intent equals, OnSessionEnded");
  },
  'LaunchRequest': function () {
    this.emit(":tell", "intent equals, OnLaunch");
  },
  'Unhandled': function() {
    this.emit(":tell", "intent equals, Unhandled");
  }
};

/** the function that alexa will call when envoking our skill.
* The execute method essentially dispatches to on of our session handlers */
exports.handler = function(event, context) {
  var alexa = Alexa.LambdaHandler(event, context);

  alexa.registerHandlers(handlers);
  alexa.dynamoDBTableName = 'my_cookbook_users';
  alexa.appId = APP_ID;
  alexa.execute();
};
