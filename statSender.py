"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

This depends on:
	psutil: http://code.google.com/p/psutil/
	pySerial: http://pyserial.sourceforge.net/
"""

import psutil, NetStat
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

KEY_NETWORK_DOWNLOAD = 'NET_DOWN'

# Send a spot every NET_DOWN_CHUNK bytes.
NET_DOWN_CHUNK = NetStat.BYTES_PER_MB / 2


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

previousBytes = NetStat.GetReceivedBytes()
def GetNetworkDownloadValue():
	"""
	Calculate a number based on the number of bytes downloaded since last
	report. Return an intensity in [0, 1.0] that is greater for more data.
	Chunk reports (so a consistent low bandwidth download will produce
	occasional pulses, not dim skitter).
	"""
	global previousBytes
	currentBytes = NetStat.GetReceivedBytes()
	dBytes = currentBytes - previousBytes
	numChunks = dBytes / NET_DOWN_CHUNK
	if numChunks > 0:
		previousBytes += numChunks*NET_DOWN_CHUNK
		intensity = 1.0 - 0.5**numChunks
		return intensity
	else:
		return None


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
		}
		networkDownValue = GetNetworkDownloadValue()
		if networkDownValue is not None:
			stats[KEY_NETWORK_DOWNLOAD] = networkDownValue

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

