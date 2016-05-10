const express = require('express')
const multer  = require('multer')
const upload = multer({ dest: 'upload/' })

const app = express()

app.get('/', function (req, res) {
    res.send('Hello World!');
});

app.post('/sound', upload.single('avatar'), function (req, res, next) {
	console.log("Beerkezo file");
    console.log("Eredeti filenev: " + req.file.originalname);
    console.log("File merete(KB): " + req.file.size/1000);
    res.end("Fajl fogadva");
})

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});
