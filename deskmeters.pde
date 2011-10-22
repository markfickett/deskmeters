/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include <newanddelete.h>
#include "DataReceiver.h"

#include <stdlib.h>

using LedController::Color;
using LedController::PatternList;
using LedController::RandomMarquee;
using LedController::MovingPeak;
using LedController::LedStrip;

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

PatternList patternList = PatternList();
RandomMarquee* marquee;
LedStrip ledStrip = LedStrip();
DataReceiver dataReceiver = DataReceiver();

int interval;

void cpuChanged(const char* value) {
	marquee->setInterval(atoi(value));
}

void networkDownloadChanged(const char* value) {
	MovingPeak* peak = new MovingPeak(Color(0x6666FF));
	if (peak == NULL) {
		Serial.print("!p");
		Serial.flush();
		return;
	}
	peak->setIntensity(atof(value));
	patternList.append(peak);
	Serial.print("+");
	Serial.flush();
}

void setup() {
	pinMode(PIN_SDI, OUTPUT);
	pinMode(PIN_CKI, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee = new RandomMarquee();
	patternList.append(marquee);
	patternList.update();
	patternList.apply(ledStrip.getColors());
	ledStrip.send(PIN_SDI, PIN_CKI);

	dataReceiver.setup();
	dataReceiver.addKey("CPU", &cpuChanged);
	dataReceiver.addKey("NET_DOWN", &networkDownloadChanged);

	delay(2000);
}

void loop() {
	dataReceiver.readAndUpdate();

	if (patternList.update()) {
		ledStrip.clear();
		patternList.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

