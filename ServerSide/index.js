const express = require('express')
const multer  = require('multer')
const upload = multer({ dest: 'upload/' })
const fs = require('fs');

const app = express()

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

app.post('/sound', upload.single('avatar'), function (req, res, next) {
	console.log("Beerkezo file");
    console.log("Eredeti filenev: " + req.file.originalname);
    console.log("File merete(KB): " + req.file.size/1024);

    fs.rename(req.file.path , __dirname + "/upload/" + req.file.originalname);

    console.log("Fajl fogadva es elmentve a " + __dirname + "/upload/" + req.file.originalname + " helyre.");
    res.end("Fajl fogadva");
})

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});
