const express = require('express');
const app = express();
const fs = require('fs');

var global_data; //data from dynamic sensor_output.json 

const PORT = 3000;
app.listen(PORT, function() {
    console.log('listening on 3000');
})

// API to fetch json data
app.get('/getData', function(req, res) {
    fs.readFile("../socket/sensor_output.json", "utf8", (err, sensor_json) => {
        if (err) {
          console.log("File read failed:", err);
          return;
        }
        global_data = sensor_json
      });
    res.send(global_data);
})
