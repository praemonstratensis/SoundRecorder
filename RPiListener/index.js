const gpio = require('rpi-gpio')
const triggeredPin = 7

gpio.on('change', function(channel, value) {
	console.log('Channel ' + channel + ' value is now ' + value)
});
gpio.setup(triggeredPin, gpio.DIR_IN, gpio.EDGE_BOTH)
