#include "Meter.h"

#include "WProgram.h"

#define ARDUINO_VOLTAGE		5.0
#define ANALOG_MAX		255.0

Meter::Meter(int outputPin, float maxCurrentAmps, float seriesResistance,
	float internalResistance) :
	pin(outputPin),
	analogFullScale(maxCurrentAmps /
		(ARDUINO_VOLTAGE/(seriesResistance + internalResistance)))
{
}

void Meter::setup() {
	pinMode(pin, OUTPUT);
	digitalWrite(pin, LOW);
}

void Meter::setValue(float value) {
	int analogValue = int(ANALOG_MAX *
		analogFullScale * constrain(value, 0.0, 1.0));
	analogWrite(pin, analogValue);
}

