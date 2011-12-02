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

PatternList patternList = PatternList();
//RandomMarquee* marquee;
//LedStrip ledStrip = LedStrip(PIN_LED_DATA, PIN_LED_CLOCK);
DataReceiver dataReceiver = DataReceiver();

/* meter			pin	full scale A	resistance */
Meter meterCpu1 = Meter(	5,	5.0/177.0,	154);
Meter meterCpu2 = Meter(	4,	5.0/255.0,	224);
Meter meterCpu3 = Meter(	3,	5.0/237.0,	224);
Meter meterCpu4 = Meter(	2,	5.0/237.0,	224);
Meter meterNetUp = Meter(	8,	5.0/531.0,	478);
Meter meterNetDn = Meter(	7,	5.0/265.0,	223);
Meter meterRam = Meter(		6,	5.0/333.0,	279);

void cpu1Changed(const char* value) { meterCpu1.setValue(atof(value)); }
void cpu2Changed(const char* value) { meterCpu2.setValue(atof(value)); }
void cpu3Changed(const char* value) { meterCpu3.setValue(atof(value)); }
void cpu4Changed(const char* value) { meterCpu4.setValue(atof(value)); }
void netUpChanged(const char* value) { meterNetUp.setValue(atof(value)); }
void netDnChanged(const char* value) { meterNetDn.setValue(atof(value)); }
void ramChanged(const char* value) { meterRam.setValue(atof(value)); }

void cpuChanged(const char* value) {
	//marquee->setInterval(atoi(value));
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

void setup() {
	//ledStrip.setup();
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	//ledStrip.clear();
	//marquee = new RandomMarquee();
	//patternList.insert(marquee);
	//patternList.update();
	//patternList.apply(ledStrip.getColors());
	//ledStrip.send();

	dataReceiver.setup();
	dataReceiver.addKey("CPU",		&cpuChanged);
	dataReceiver.addKey("CPU1",		&cpu1Changed);
	dataReceiver.addKey("CPU2",		&cpu2Changed);
	dataReceiver.addKey("CPU3",		&cpu3Changed);
	dataReceiver.addKey("CPU4",		&cpu4Changed);
	dataReceiver.addKey("NET_UP",		&netUpChanged);
	dataReceiver.addKey("NET_DOWN",		&netDnChanged);
	dataReceiver.addKey("RAM",		&ramChanged);

	meterCpu1.setup();
	meterCpu2.setup();
	meterCpu3.setup();
	meterCpu4.setup();
	meterNetUp.setup();
	meterNetDn.setup();
	meterRam.setup();
}

void loop() {
	dataReceiver.readAndUpdate();

	/*
	if (patternList.update()) {
		ledStrip.clear();
		patternList.apply(ledStrip.getColors());
		ledStrip.send();
	}
	*/
}

