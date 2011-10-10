/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include "SerialBaud.h"

#include <stdlib.h>

using LedController::Color;
using LedController::RandomMarquee;
using LedController::LedStrip;

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

#define INTERVAL_MAX	300

RandomMarquee marquee = RandomMarquee();
LedStrip ledStrip = LedStrip();

int interval;

void setup() {
	pinMode(PIN_SDI, OUTPUT);
	pinMode(PIN_CKI, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee.update();
	marquee.apply(ledStrip.getColors());
	ledStrip.send(PIN_SDI, PIN_CKI);

	Serial.begin(SERIAL_BAUD);
	Serial.println("Hello! Setup complete.");

	delay(2000);

	interval = INTERVAL_MAX;
}

void loop() {
	setMarqueeSpeed();

	if (marquee.update()) {
		ledStrip.clear();
		marquee.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

#define READ_BUFFER_SIZE	255
char readBuffer[READ_BUFFER_SIZE];
void setMarqueeSpeed() {
	static int readIndex = 0;
	static int valueIndex = 0;
	while (Serial.available() > 0) {
		int c = Serial.read();
		if (c == '\n' || readIndex+1 >= READ_BUFFER_SIZE) {
			readBuffer[readIndex] = '\0';

			float value = atof(readBuffer + valueIndex);
			Serial.print("Got ");
			Serial.print(value);
			value = 1.0 - value/100.0;
			value = value*value*value;
			interval = int(INTERVAL_MAX * value);
			Serial.print(" interval ");
			Serial.println(interval);

			marquee.setInterval(interval);

			valueIndex = readIndex = 0;
			Serial.flush();
			break;
		} else {
			readBuffer[readIndex] = c;
			readIndex++;
			if (c == '\t') {
				valueIndex = readIndex;
			}
		}
	}
}

