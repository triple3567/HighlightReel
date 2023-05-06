const express = require("express");
const { get } = require("http");
const app = express();
const bodyParser = require('body-parser');
var multer = require('multer');
const { executionAsyncId } = require("async_hooks");
var upload = multer();
var hostname = '192.168.4.1';
var PORT = 8000;

// for parsing application/json
app.use(bodyParser.json())

// for parsing application/xwww-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// for parsing multipart/form-data
app.use(upload.array()); 

app.use("/home/pi/HighlightReel/web_dash/res", express.static("res"));
app.use("/home/pi/HighlightReel/web_dash/public", express.static("public"));

app.get("/", (req, res) => {
    var execSync = require('child_process').execSync;

    let result = String(execSync("/home/pi/HighlightReel/web_dash/scripts/check_highlight_reel_status.sh"))

    if(result.localeCompare("running\n") === 0){
        res.sendFile("/home/pi/HighlightReel/web_dash/html/home_online.html");
    }
    else if(result.localeCompare("dead\n") === 0){
        res.sendFile("/home/pi/HighlightReel/web_dash/html/home_offline.html")
    }
    else{
        console.log("Error in GET request to /")
    }
});

app.post("/configureWifi", (req, res) => {
    console.log("recieved post request to /configureWifi")
    console.log(req.body.ssid)
    console.log(req.body.psk)

    var exec = require('child_process').exec;
    exec("/home/pi/HighlightReel/web_dash/scripts/configure_wifi.sh" + " \"" + req.body.ssid + "\"  \"" + req.body.psk + "\"", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.sendFile("/home/pi/HighlightReel/web_dash/html/connecting.html")
});

app.get("/camera", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/camera.html");
});


app.get("/camera/refresh", (req,res) =>{
    var execSync = require('child_process').execSync;

    execSync("/home/pi/HighlightReel/web_dash/scripts/capture.sh")
    console.log("done")

    res.sendFile("/home/pi/HighlightReel/web_dash/res/capture.jpg")
})

app.get("/restart.html", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/restart.html")
})
app.get("/restart", (req, res) => {
    var exec = require('child_process').exec;

    exec("/home/pi/HighlightReel/web_dash/html/restart.html", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.get("/stop.html", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/stop.html")
})
app.get("/stop", (req, res) => {
    var exec = require('child_process').exec;

    exec("/home/pi/HighlightReel/web_dash/scripts/stop_core.sh", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.get("/reboot", (req, res) => {
    var exec = require('child_process').exec;

    exec("/home/pi/HighlightReel/web_dash/scripts/reboot.sh", 
    function(err, stdout, stderr) {
        console.log(stdout)
        console.log(stderr)
    })
    res.sendFile("/home/pi/HighlightReel/web_dash/html/restart.html")
})

app.get("/update_and_reboot", (req, res) => {
    var exec = require('child_process').exec;
    var execSync = require('child_process').execSync;
    
    execSync("/home/pi/HighlightReel/web_dash/scripts/checkout_main.sh")

    exec("/home/pi/HighlightReel/web_dash/scripts/reboot.sh", 
    function(err, stdout, stderr) {
        console.log(stdout)
        console.log(stderr)
    })
    res.sendFile("/home/pi/HighlightReel/web_dash/html/restart.html")
})


app.get("/wifi-list", (req, res) => {
    var execSync = require('child_process').execSync;

    let result = String(execSync("/home/pi/HighlightReel/web_dash/scripts/scan_wifi.sh"))

    result = result.split('ESSID:').join('')

    let result_array = []
    let search_index = 0
    index = result.indexOf("\"", search_index)
    while(index != -1){
        search_index = index + 1
        let word_start = index + 1
        let word_end = result.indexOf("\"", search_index)

        console.log(result.substring(word_start, word_end))
        result_array.push(result.substring(word_start, word_end))

        search_index = word_end + 1
        index = result.indexOf("\"", search_index)
    }
    console.log(result_array)
    res.send(result_array)
});

app.get("/wifi-settings", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/wifi-settings.html")
})

app.get("/start.html", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/start.html")
})

app.get("/stop.html", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/stop.html")
})

app.get("/stop_and_settings.html", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/stop_and_settings.html")
})

app.get("/start", (req, res) => {
    var exec = require('child_process').exec;

    exec("/home/pi/HighlightReel/web_dash/scripts/start_core.sh", 
        function(err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
    })

    res.send()
});

app.get("/settings", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/settings.html")
})

app.post("/register_wristband", (req, res) => {
    var execSync = require('child_process').execSync;

    console.log("listening for wristband")

    let result = String(execSync("/usr/bin/python3 /home/pi/HighlightReel/web_dash/scripts/register_wristband.py"))

    console.log("Heard " + result)
    res.send(result)
})

app.post("/delete_wristband", (req, res) => {
    var execSync = require('child_process').execSync;

    console.log(req.body.wristband)

    let result = String(execSync("/usr/bin/python3 /home/pi/HighlightReel/web_dash/scripts/delete_wristband.py \"" + String(req.body.wristband) + "\""))

    res.send()
})

app.get("/wristbands", (req, res) =>{
    const fs = require('fs');

    fs.readFile('/home/pi/HighlightReel/core/res/wristband_codes_custom.json', 'utf8', (err, data) => {
        if (err) throw err;
        const wristbandCodes = JSON.parse(data);
        res.send(wristbandCodes)
    });
})

app.get("/wristband_settings", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/wristband_settings.html")
})

app.get("/poolID_settings", (req, res) => {
    res.sendFile("/home/pi/HighlightReel/web_dash/html/poolID_settings.html")
})

app.get("/poolID", (req, res) => {
    const fs = require('fs');

    fs.readFile("/home/pi/HighlightReel/core/res/config-custom.json", 'utf8', (err, data) => {
        if (err) throw err;
        const config = JSON.parse(data)
        const poolId = config["poolID"]

        if(poolId == null){
            res.send("No Pool ID Set!")
        }
        else{
            res.send(poolId)
        }
    })
})

app.post("/poolID", (req, res) => {
    const fs = require('fs');

    var name = "/home/pi/HighlightReel/core/res/config.json"
    
    fs.readFile(name, 'utf8', (err, data) => {
        if (err) throw err;
        var config = JSON.parse(data)

        config['poolID'] = req.body.poolID

        var modifiedConfig = JSON.stringify(config, null, "\t")
        fs.writeFileSync(name, modifiedConfig)
        res.send()
    })
})


app.listen(PORT, hostname, () => {
    console.log("Application started and Listening on " + hostname +":" + PORT);
  });
