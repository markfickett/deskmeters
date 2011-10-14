#include "DataReceiver.h"

#include "WProgram.h"

DataReceiver::DataReceiver() : numListeners(0), readIndex(0), valueIndex(0)
{
};

void DataReceiver::setup() {
	Serial.begin(SERIAL_BAUD);
	Serial.println("Listening for data on serial!");
}

void DataReceiver::addKey(const char* key, callbackPtr_t callbackPtr) {
	if (numListeners >= MAX_KEYS) {
		Serial.print("Error: DataReceiver out of space,"
			" cannot register key \"");
		Serial.print(key);
		Serial.println("\".");
		return;
	}
	if (strlen(key) >= STR_SIZE+1) {
		Serial.print("Error: DataReceiver can't handle key \"");
		Serial.print(key);
		Serial.print("\" of length ");
		Serial.print(strlen(key));
		Serial.print(" which won't fit in a size ");
		Serial.print(STR_SIZE);
		Serial.println(" buffer.");
	}
	strcpy(listeners[numListeners].key, key);
	listeners[numListeners].callbackPtr = callbackPtr;
	numListeners++;
}

void DataReceiver::readAndUpdate() {
	while (Serial.available() > 0) {
		int c = Serial.read();
		if (c == '\n' || readIndex+1 >= READ_BUFFER_SIZE) {
			readBuffer[readIndex] = '\0';

			findAndCallCallback(readBuffer,
				readBuffer + valueIndex);

			valueIndex = readIndex = 0;
			//Serial.flush();
			break;
		} else {
			if (c == '\t') {
				valueIndex = readIndex+1;
				c = '\0';
			}
			readBuffer[readIndex] = c;
			readIndex++;
		}
	}
}

void DataReceiver::findAndCallCallback(const char* key, const char* value) {
	for(int i = 0; i < numListeners; i++) {
		if (strcmp(key, listeners[i].key) == 0) {
			(*listeners[i].callbackPtr)(value);
			return;
		}
	}
	Serial.print("Warning: DataReceiver found no handler for key \"");
	Serial.print(key);
	Serial.print("\" (sent with value \"");
	Serial.print(value);
	Serial.println("\", ignoring.");
}

