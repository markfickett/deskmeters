Desk Meters
===========

This controls, via Arduino, analog panel meters and an addressable LED strip. They show stats for a desktop computer: CPU, RAM, and network usage.

![panel meter pair, moving](http://farm8.staticflickr.com/7006/6705796061_f5e1f21770.jpg)

Panel meters for two CPU cores. Photo [courtesy of Matthew Fickett on flickr](http://www.flickr.com/photos/capybararancher/6705796061/). More details and photos [on his page for this project](http://www.matthewfickett.com/2012/01/desk-with-meters/).

Desktop Computer (Python)
-------------------------

In Python, the controller fetches various stats (in part using [psutil](from http://code.google.com/p/psutil/) ). It then uses the Python side of [DataReceiver](https://github.com/markfickett/DataReceiver) to pack the stats as strings and send them to the Arduino.

Arduino
-------

The Arduino uses its half of DataReceiver to register callbacks for changes to the stats. It uses [PWM](http://arduino.cc/en/Tutorial/PWM) to control the current through each panel meter (previously calibrated to determine necessary current).

The circuit for each meter is: (1) Arduino digital PWM output pin, (2) resistor, (3) panel meter + terminal, (4) panel meter - terminal, and (5) Arduino ground. The [shunt](http://en.wikipedia.org/wiki/Shunt_\(electrical\)\#Use_in_current_measuring) in each meter was clipped to bring its full range within controllable range of the Arduino, and then a resistor was added in series to bring the ranges closer (increasing fidelity and reducing over-current danger)\*.

The Arduino uses [LED Controller](https://github.com/markfickett/LED-Controller) to run colors along the LED strip. (The LED strip's hardware connection is documented in that library.)

\* For example, a meter with an internal resistance of 5 ohms and a full-scale range of 10mA might get:

	I > V/R	(We want to be able to deliver just over the max current.)
	R < V/I
	R + 5 ohms < 5V / 10mA

So we pick a 470 ohm resistor (rounding down to the nearest standard value).

