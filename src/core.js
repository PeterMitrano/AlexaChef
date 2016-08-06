/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

var Request = require('request');

var api_url = 'https://6peln83v5l.execute-api.us-east-1.amazonaws.com/dev/';

module.exports  = {
  'api_headers': {
    "x-api-key": 'JK, LOL'
  },
  'api_url': 'https://6peln83v5l.execute-api.us-east-1.amazonaws.com/dev/',
  'endpoints': {
    'recipe': 'recipes',
    'search': 'search'
  },
  'states': {
      ASK_MAKE_COOKBOOK: '_ASK_MAKE_COOKBOOK',
      ASK_SEARCH: '_ASK_SEARCH',
      ASK_TUTORIAL: '_ASK_TUTORIAL',
      ASK_MAKE_SOMETHING: '_ASK_MAKE_SOMETHING',
      INGREDIENTS_OR_INSTRUCTIONS: '_INGREDIENTS_OR_INSTRUCTIONS',
      INITIAL_STATE: '_INITIAL_STATE',
      NEW_RECIPE: '_NEW_RECIPE',
      PROMPT_FOR_START: '_PROMPT_FOR_START',
      SEARCH_ONLINE: '_SEARCH_ONLINE',
      TELL_TUTORIAL: '_TELL_TUTORIAL'
  },
  'makeRequest': function(endpoint, my_callback){
    var options = {
        'url': this.api_url + endpoint,
        'method': 'GET',
        'headers': this.api_headers
    };
    Request(options, function(err, response, body) {
      console.log(JSON.stringify(body,null,2));
      my_callback(err, response, body);
    });
  },

  /**
   * This function checks if this is the first ever time the user has launched
   * our app.
   * @param {handlerContext} handlerContext - the session related info
   */
  'firstTimeIntroductionIfNeeded': function (handlerContext) {
    if (handlerContext.attributes.invocations === undefined || handlerContext.attributes.invocations === 0) {
      handlerContext.handler.state = this.states.ASK_TUTORIAL;
      handlerContext.attributes.invocations = 1;
      handlerContext.emit(":ask", "Hi, I'm your new cookbook. Would you like to start off with a tutorial?");
      handlerContext.emit(':saveState', true);
      return true;
    }

    return false;
  }
};
