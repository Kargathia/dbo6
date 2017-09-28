var express = require('express');
var app = express();
var fs = require("fs");
var faker = require("faker");
var bodyParser = require('body-parser');

var jsonParser = bodyParser.json()

app.post('/fake', jsonParser, function (req, res) {
    if (!req.body) return res.sendStatus(400);
    console.log(req.body.type);
    res.send(faker.fake('{{' + req.body.type + '}}'));
  })

var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Faker app listening at http://%s:%s", host, port)

})