const express = require("express");
const { get } = require("http");
const app = express();
const bodyParser = require('body-parser');
var multer = require('multer');
var upload = multer();
var hostname = '192.168.4.1';
var PORT = 8000;

// for parsing application/json
app.use(bodyParser.json())

// for parsing application/xwww-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// for parsing multipart/form-data
app.use(upload.array()); 

app.use("/res", express.static("res"));
app.use("/public", express.static("public"));

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/html/index.html");
});

app.post("/configureWifi", (req, res) => {
    var exec = require('child_process').exec;
    exec("scripts/configure_wifi.sh" + " " + req.body.ssid + " " + req.body.psk, 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.sendFile(__dirname + "/html/connecting.html")
});

app.get("/camera", (req, res) => {
    res.sendFile(__dirname + "/html/camera.html");
});


app.get("/camera/refresh", (req,res) =>{
    var execSync = require('child_process').execSync;

    execSync("scripts/capture.sh")
    console.log("done")

    res.sendFile("/home/pi/HighlightReel/web_dash/res/capture.jpg")
})

app.get("/restart.html", (req, res) => {
    res.sendFile(__dirname + "/html/restart.html")
})
app.get("/restart", (req, res) => {
    var exec = require('child_process').exec;

    exec("scripts/restart.sh", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.get("/stop.html", (req, res) => {
    res.sendFile(__dirname + "/html/stop.html")
})
app.get("/stop", (req, res) => {
    var exec = require('child_process').exec;

    exec("scripts/stop_core.sh", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.get("/start.html", (req, res) => {
    res.sendFile(__dirname + "/html/start.html")
})
app.get("/start", (req, res) => {
    var exec = require('child_process').exec;

    exec("scripts/start_core.sh", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.listen(PORT, hostname, () => {
    console.log("Application started and Listening on " + hostname +":" + PORT);
  });
