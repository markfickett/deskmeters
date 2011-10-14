/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include "DataReceiver.h"

#include <stdlib.h>

using LedController::Color;
using LedController::RandomMarquee;
using LedController::LedStrip;

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

RandomMarquee marquee = RandomMarquee();
LedStrip ledStrip = LedStrip();
DataReceiver dataReceiver = DataReceiver();

int interval;

void cpuChanged(const char* value) {
	marquee.setInterval(atoi(value));
}

void networkUploadChanged(const char* value) {
}

void setup() {
	pinMode(PIN_SDI, OUTPUT);
	pinMode(PIN_CKI, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee.update();
	marquee.apply(ledStrip.getColors());
	ledStrip.send(PIN_SDI, PIN_CKI);

	dataReceiver.setup();
	dataReceiver.addKey("CPU", &cpuChanged);
	dataReceiver.addKey("NET_UP", &networkUploadChanged);

	delay(2000);
}

void loop() {
	dataReceiver.readAndUpdate();

	if (marquee.update()) {
		ledStrip.clear();
		marquee.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

