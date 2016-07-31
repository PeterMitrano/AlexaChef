/**
 * @fileOverview
 * @author Peter Mitrano- mitrnanopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * For telling user about tutorial. this hasn't been properly thought out yet.
 */
module.exports  = Alexa.CreateStateHandler(Core.states.TELL_TUTORIAL, {
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. I was telling you about how to use this app");
  }
});
