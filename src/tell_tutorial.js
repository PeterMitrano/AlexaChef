var Core = require('./core');
var Alexa = require('./alexa');

module.exports  = Alexa.CreateStateHandler(Core.states.TELL_TUTORIAL, {
  'Unhandled': function() {
    this.emit(":tell", "I'm confused. I was telling you about how to use this app");
  }
});
