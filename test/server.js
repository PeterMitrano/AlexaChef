'use strict';

let express = require('express');
let bodyParser = require('body-parser');
let path = require('path');
let app = express();
let index = require("../src/index");
let generator = require("./generate_utterances");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.set('views', path.join(__dirname,'views'));
app.set('view engine', 'ejs');

app.listen(3000, function () {
  console.log('Listening on port 3000.');
});
app.get('/', function(req, res) {
  res.render('test', {
    "app": index.name,
    "appId": index.appId,
    "schema": JSON.stringify(generator.schema(), null, 2),
    "intents": generator.intents(),
    "utterances": generator.generate(),
  });
});
app.post('/', function(req, res) {
  index.handler(req.body, {}, function(error, data) {
    // send back to webpage
    res.json(data || error).send();
  });
});
