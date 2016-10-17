const express = require('express')
const multer  = require('multer')
const config  = require('./config.json')
const path  = require('path')
const upload = multer({ dest: 'upload/' })
const fs = require('fs');
const exec = require('child_process').exec;

const app = express()

var postHookDir = __dirname + path.sep + 'upload-post.d'

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, '/upload')
  },
  filename: function (req, file, cb) {
    cb(null, req.file.originalname)
  }
})

app.get('/', function (req, res) {
    res.send('Hello World!');
});

app.post('/recording/upload', upload.single('sound_file'), function (req, res, next) {
    console.log("Beerkezo hangfile");
    console.log("Eredeti filenev: " + req.file.originalname);
    console.log("File merete(KB): " + req.file.size/1024);

    fs.rename(req.file.path , __dirname + "/upload/" + req.file.originalname);

    console.log("Fajl fogadva es elmentve a " + __dirname + "/upload/" + req.file.originalname + " helyre.");
    res.end("Fajl fogadva");

})

app.listen(config.port, function () {
    console.log('Server listening on port '+ config.port +'!');
});