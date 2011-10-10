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
UPDATE_WINDOW = 20

KEY_CPU = 'CPU'
SERIAL_DEVICE = '/dev/tty.usbmodemfd131'
SERIAL_BAUD_FILE = 'SerialBaud.h'
SERIAL_BAUD_NAME = 'SERIAL_BAUD'
TIMEOUT = 0 # non-blocking read

with open(SERIAL_BAUD_FILE) as baudDefineFile:
	tokens = ''.join(baudDefineFile.readlines()).split()
	nameIndex = tokens.index(SERIAL_BAUD_NAME)
	serialBaud = int(tokens[nameIndex+1])

if __name__ == '__main__':
	arduinoSerial = serial.Serial(SERIAL_DEVICE, serialBaud,
		timeout=TIMEOUT)
	cpuValues = [0.0,]*UPDATE_WINDOW
	while True:
		cpuValues = cpuValues[1:]
		cpuValues.append(psutil.cpu_percent())
		stats = {
			KEY_CPU: sum(cpuValues)/len(cpuValues),
		}
		statsStr = '\n'.join(
			['%s\t%s' % (label, value) for label, value
				in stats.iteritems()]) + '\n'
		arduinoSerial.write(statsStr)
		print 'Sent ', statsStr,

		lines = ''
		line = arduinoSerial.readline()
		while line:
			lines += line
			line = arduinoSerial.readline()
		print lines
		time.sleep(UPDATE_INTERVAL_SECS)
	arduinoSerial.close()

