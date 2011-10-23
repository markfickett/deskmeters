#pragma once

#include "SerialBaud.h"

#define MAX_KEYS		3
#define STR_SIZE		20
#define READ_BUFFER_SIZE	255

typedef void(*callbackPtr_t)(const char*);

struct Listener {
	char key[STR_SIZE];
	callbackPtr_t callbackPtr;
};

class DataReceiver {
	private:
		int numListeners;
		struct Listener listeners[MAX_KEYS];

		char readBuffer[READ_BUFFER_SIZE];
		int readIndex;
		int valueIndex;

		void findAndCallCallback(const char* key, const char* value);

	public:
		DataReceiver();

		void setup();

		void addKey(const char* key, callbackPtr_t callbackPtr);

		void readAndUpdate();
};

