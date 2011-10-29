/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include <newanddelete.h>
#include <DataReceiver.h>

#include <stdlib.h>

using LedController::Color;
using LedController::PatternList;
using LedController::RandomMarquee;
using LedController::MovingPeak;
using LedController::LedStrip;

#define PIN_LED_DATA	2	// red data wire, SDI (not the red 5V wire!)
#define PIN_LED_CLOCK	3	// green wire, CKI
#define PIN_STATUS_LED	13	// on board LED

PatternList patternList = PatternList();
RandomMarquee* marquee;
LedStrip ledStrip = LedStrip();
DataReceiver dataReceiver = DataReceiver();

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
	pinMode(PIN_LED_DATA, OUTPUT);
	pinMode(PIN_LED_CLOCK, OUTPUT);
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	ledStrip.clear();
	marquee = new RandomMarquee();
	patternList.insert(marquee);
	patternList.update();
	patternList.apply(ledStrip.getColors());
	ledStrip.send(PIN_LED_DATA, PIN_LED_CLOCK);

	dataReceiver.setup();
	dataReceiver.addKey("CPU", &cpuChanged);
	dataReceiver.addKey("NET_DOWN", &networkDownloadChanged);
	dataReceiver.addKey("NET_UP", &networkUploadChanged);
}

void loop() {
	dataReceiver.readAndUpdate();

	if (patternList.update()) {
		ledStrip.clear();
		patternList.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);
	}
}

