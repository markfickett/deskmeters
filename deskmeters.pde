/**
 * Control analog meters and addressable LED strip lights to reflect state
 * of a computer (CPU and RAM usage, etc). Receive data over Serial.
 */

#include <ledcontroller.h>

using LedController::Color;
using LedController::RandomMarquee;
using LedController::LedStrip;

#define PIN_SDI 2		// Red data wire (not the red 5V wire!)
#define PIN_CKI 3		// Green wire
#define PIN_STATUS_LED 13	// On board LED

#define INTERVAL	250

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

	Serial.begin(9600);
	Serial.println("Hello! Setup complete.");

	delay(2000);

	interval = INTERVAL;
}

void loop() {

	if (marquee.update()) {
		ledStrip.clear();
		marquee.apply(ledStrip.getColors());
		ledStrip.send(PIN_SDI, PIN_CKI);

		interval--;
		if (interval == 0) {
			interval = INTERVAL;
		}
		marquee.setInterval(interval);
	}
}

