// Initialise Blynk
var blynkLib = require('blynk-library');
var sensorLib = require('node-dht-sensor');
var Gpio = require('/home/pi/node_modules/onoff').Gpio,
  relay = new Gpio(30, 'out');

var AUTH = '0ab7483e81cc4406a93533447c040ee1';

// Setup Blynk connection
var blynk = new blynkLib.Blynk(AUTH);

// Setup sensor, exit if failed
var sensorType = 22; // 11 for DHT11, 22 for DHT22 and AM2302
var sensorPin  = 28;  // The GPIO pin number for sensor signal
if (!sensorLib.initialize(sensorType, sensorPin)) {
    console.warn('Failed to initialize sensor');
    process.exit(1);
}

// Automatically update sensor value every 30 seconds
setInterval(function() {
    var readout = sensorLib.read();
    blynk.virtualWrite(3, readout.temperature.toFixed(1));
    blynk.virtualWrite(4, readout.humidity.toFixed(1));
    
    console.log('Temperature:', readout.temperature.toFixed(1) + 'C');
    console.log('Humidity:   ', readout.humidity.toFixed(1)    + '%');
}, 30000);

//Re-route GPIO30 to a VirtualPin to allow control of relay via the Blynk app, which can only control up to GPIO27 natively
var v1 = new blynk.VirtualPin(1);  // virtual pin to control GPIO 30
v1.on('write', function() {
        if(relay.readSync() == 0) {  // toggle gpio 30 from high to low
                relay.writeSync(1);
        }
        else {
                relay.writeSync(0);
        }
});
