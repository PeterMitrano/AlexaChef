'use strict';

let index = require("../src/index");
let core = require("../src/core");
let generator = require("../util/generate_utterances");

let chai = require('chai');
let expect = chai.expect;

let LaunchType = "LaunchRequest";
let IntentType = "IntentRequest";
let EndType = "EndSessionRequest";

describe('Launch', function() {
  it("launch request", function (done) {
    //create a request and send it to my handler
    let req = generator.request().withAppId(index.appId).withType(LaunchType).withUser("1").withNew();
    index.handler(req, {}, function(error, data){
      expect(error).to.equal(null);
      expect(data.response.outputSpeech.ssml).to.not.equal(undefined);
      done();
    }, true);
  });
  it("end session request", function (done) {
    //create a request and send it to my handler
    let req = generator.request().withAppId(index.appId).withType(EndType).withUser("1").withNew();
    index.handler(req, {}, function(error, data){
      expect(error).to.equal(null);
      expect(data.response.outputSpeech.ssml).to.not.equal(undefined);
      done();
    }, true);
  });
  it("intent requests with empty slots", function (done) {
    done();

    //create a request and send it to my handler
    let req = generator.request().withAppId(index.appId).withType(IntentType).withUser("1").withNew();
    let intents = generator.intents();

    let completed_requests = 0;
    let keys = Object.keys(intents);
    keys.forEach(function(key) {
      let meta_intent = intents[key];
      let intent  = generator.intent(meta_intent.name)
      let intent_req = req.withIntent(intent);
      index.handler(intent_req, {}, function(error, data){
        expect(error).to.equal(null);
        expect(data.response.outputSpeech.ssml).to.not.equal(undefined);
        completed_requests++;
        if (completed_requests === keys.length - 1) {
        }
      }, true);
    });
  });
});
