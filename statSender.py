"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py .
"""

from Manifest import serial
from Manifest import time
from Manifest import CpuValue, NetworkValues

UPDATE_INTERVAL_SECS = 0.01

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'
SERIAL_BAUD_FILE = 'SerialBaud.h'
SERIAL_BAUD_NAME = 'SERIAL_BAUD'
TIMEOUT = 0 # non-blocking read


STAT_SOURCES = {
	'CPU':		CpuValue.GetCpuValue,
	'NET_DOWN':	NetworkValues.GetDownloadValue,
	'NET_UP':	NetworkValues.GetUploadValue,
}


if __name__ == '__main__':
	with open(SERIAL_BAUD_FILE) as baudDefineFile:
		tokens = ''.join(baudDefineFile.readlines()).split()
		nameIndex = tokens.index(SERIAL_BAUD_NAME)
		serialBaud = int(tokens[nameIndex+1])
	arduinoSerial = serial.Serial(SERIAL_DEVICE, serialBaud,
		timeout=TIMEOUT)

	while True:
		stats = ''
		for keyName, getValueFn in STAT_SOURCES.iteritems():
			value = getValueFn()
			if value is not None:
				stats += '%s\t%s\n' % (keyName, value)

		arduinoSerial.write(stats)

		lines = ''
		line = arduinoSerial.readline()
		while line:
			lines += line
			line = arduinoSerial.readline()
		if lines:
			print lines

		time.sleep(UPDATE_INTERVAL_SECS)
	arduinoSerial.close()

