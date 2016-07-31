/**
 * @fileOverview
 * @author Peter Mitrano- mitranopeter@gmail.com
 */

'use strict';

var Core = require('../core');
var Alexa = require('../alexa');

/**
 * For asking user about tutorial. this hasn't been properly thought out yet.
 */
module.exports  = Alexa.CreateStateHandler(Core.states.TELL_TUTORIAL, {
  'Unhandled': function() {
    this.handler.state = Core.states.INITIAL_STATE;
    this.emit(":ask", "This stae is unimplemented.");
  }
});
