/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include <newanddelete.h>
#include <DataReceiver.h>

#include <stdlib.h>

#include "Meter.h"

using LedController::Color;
using LedController::PatternList;
using LedController::RandomMarquee;
using LedController::MovingPeak;
using LedController::LedStrip;

#define PIN_LED_DATA	2	// red data wire, SDI (not the red 5V wire!)
#define PIN_LED_CLOCK	3	// green wire, CKI
#define PIN_STATUS_LED	13	// on board LED
#define PIN_METER	10

PatternList patternList = PatternList();
RandomMarquee* marquee;
LedStrip ledStrip = LedStrip(PIN_LED_DATA, PIN_LED_CLOCK);
DataReceiver dataReceiver = DataReceiver();
Meter meter = Meter(PIN_METER, 1.16E-3, 4.3E3, 5.0);

void cpu0Changed(const char* value) {
	meter.setValue(atof(value));
}

void cpuChanged(const char* value) {
	marquee->setInterval(atoi(value));
}

void addPeak(const LedController::Color& color, float intensity, bool reverse) {
	MovingPeak* peak = new MovingPeak(color);
	if (peak == NULL) {
		Serial.print("!p");
		Serial.flush();
		return;
	}
	peak->setIntensity(intensity);
	if (reverse) {
		peak->setPosition(STRIP_LENGTH-1);
		peak->setIncrement(-1);
	}
	patternList.insert(peak);
	Serial.print("+");
	Serial.flush();
}

void networkDownloadChanged(const char* value) {
	addPeak(Color(0x6666FF), atof(value), false);
}

void networkUploadChanged(const char* value) {
	addPeak(Color(0xFF2222), atof(value), true);
}

void setup() {
	ledStrip.setup();
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee = new RandomMarquee();
	patternList.insert(marquee);
	patternList.update();
	patternList.apply(ledStrip.getColors());
	ledStrip.send();

	dataReceiver.setup();
	dataReceiver.addKey("CPU", &cpuChanged);
	dataReceiver.addKey("NET_DOWN", &networkDownloadChanged);
	dataReceiver.addKey("NET_UP", &networkUploadChanged);
	dataReceiver.addKey("CPU0", &cpu0Changed);

	meter.setup();
}

void loop() {
	dataReceiver.readAndUpdate();

	if (patternList.update()) {
		ledStrip.clear();
		patternList.apply(ledStrip.getColors());
		ledStrip.send();
	}
}

