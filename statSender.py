"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

This depends on:
	psutil: http://code.google.com/p/psutil/
	pySerial: http://pyserial.sourceforge.net/
"""

import psutil
import serial
import time

UPDATE_INTERVAL_SECS = 0.01
UPDATE_WINDOW = 8

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'
SERIAL_BAUD_FILE = 'SerialBaud.h'
SERIAL_BAUD_NAME = 'SERIAL_BAUD'
TIMEOUT = 0 # non-blocking read

KEY_CPU = 'CPU'
CPU_MARQUEE_INTERVAL_MAX = 300

KEY_NETWORK_UPLOAD = 'NET_UP'


cpuValues = None
def GetCpuValue():
	global cpuValues
	if cpuValues is None:
		cpuValues = [0.0,]*UPDATE_WINDOW
	cpuValues = cpuValues[1:]
	cpuValues.append(psutil.cpu_percent())

	cpuAverage = sum(cpuValues)/len(cpuValues)
	scaleFactor = (1.0 - cpuAverage/100.0)**3
	return int(scaleFactor*CPU_MARQUEE_INTERVAL_MAX)

def GetNetworkUploadValue():
	return 1

with open(SERIAL_BAUD_FILE) as baudDefineFile:
	tokens = ''.join(baudDefineFile.readlines()).split()
	nameIndex = tokens.index(SERIAL_BAUD_NAME)
	serialBaud = int(tokens[nameIndex+1])

if __name__ == '__main__':
	arduinoSerial = serial.Serial(SERIAL_DEVICE, serialBaud,
		timeout=TIMEOUT)
	while True:
		stats = {
			KEY_CPU: GetCpuValue(),
			KEY_NETWORK_UPLOAD: GetNetworkUploadValue(),
		}
		statsStr = '\n'.join(
			['%s\t%s' % (label, value) for label, value
				in stats.iteritems()]) + '\n'
		arduinoSerial.write(statsStr)

		lines = ''
		line = arduinoSerial.readline()
		while line:
			lines += line
			line = arduinoSerial.readline()
		if lines:
			print lines
		time.sleep(UPDATE_INTERVAL_SECS)
	arduinoSerial.close()

