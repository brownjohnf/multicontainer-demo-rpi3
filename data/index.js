'use strict';

const express = require('express');
const { exec } = require('child_process');

const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

period = parseInt(process.env.PERIOD) || 500;

let sendTemp = function(socket, data) {
   //data.color = '#FF0000'
  socket.emit('temperature', data);
}

let getCpuTemp = function(socket) {
  exec('cat /sys/class/thermal/thermal_zone*/temp', (err, stdout) => {
    if (err) throw err;
    let data = {
      t: parseFloat(stdout) / 1000
    };
    sendTemp(socket, data);
  });
};

let getRandomTemp = function(socket) {
  let data = {
    t: (20 + Math.floor(Math.random() * 30))
  };
  sendTemp(socket, data);
};

io.on('connection', function(socket) {
  console.log('a user connected');

  let dataLoop = setInterval(function() {
    //getCpuTemp(socket);
    getRandomTemp(socket);
  }, period);

  socket.on('disconnect', function() {
      console.log('a user disconnected');
      clearInterval(dataLoop);
   });
});

server.listen(8080);
