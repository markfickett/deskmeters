/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>
#include <DataReceiver.h>

#include <stdlib.h>

#include "Meter.h"

#define PIN_LED_DATA	51	// red data wire, SDI (not the red 5V wire!)
#define PIN_LED_CLOCK	49	// green wire, CKI
#define PIN_STATUS_LED	13	// on board LED

DataReceiver<9> dataReceiver;
LedController::LedPiper ledPiper(PIN_LED_DATA, PIN_LED_CLOCK);

/* meter			pin	max analog value, fraction of 1.0 */
Meter meterCpu1 = Meter(	5,	1.0);
Meter meterCpu2 = Meter(	4,	1.0);
Meter meterCpu3 = Meter(	3,	1.0);
Meter meterCpu4 = Meter(	2,	1.0);
Meter meterRam = Meter(		8,	1.0);
Meter meterNetUp = Meter(	7,	0.94);
Meter meterNetDn = Meter(	6,	1.0);
Meter meterMinecraft = Meter(	9,	0.87);

void minecraftChanged(size_t unusedSize, const char* value) {
	meterMinecraft.setValue(atof(value));
}
void cpu1Changed(size_t unusedSize, const char* value) {
	meterCpu1.setValue(atof(value));
}
void cpu2Changed(size_t unusedSize, const char* value) {
	meterCpu2.setValue(atof(value));
}
void cpu3Changed(size_t unusedSize, const char* value) {
	meterCpu3.setValue(atof(value));
}
void cpu4Changed(size_t unusedSize, const char* value) {
	meterCpu4.setValue(atof(value));
}
void netUpChanged(size_t unusedSize, const char* value) {
	meterNetUp.setValue(atof(value));
}
void netDnChanged(size_t unusedSize, const char* value) {
	meterNetDn.setValue(atof(value));
}
void ramChanged(size_t unusedSize, const char* value) {
	meterRam.setValue(atof(value));
}

void ledColorsChanged(size_t size, const char* colorBytes) {
  ledPiper.setColorsAndSend(size, colorBytes);
}

void setup() {
	pinMode(PIN_STATUS_LED, OUTPUT);

	randomSeed(analogRead(0));

	dataReceiver.setup();
	dataReceiver.addKey(DATA_RECEIVER_COLOR_KEY,		&ledColorsChanged);
	dataReceiver.addKey("MINECRAFT",	&minecraftChanged);
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
	meterMinecraft.setup();

	dataReceiver.sendReady();
}

void loop() {
	dataReceiver.readAndUpdate();
}

