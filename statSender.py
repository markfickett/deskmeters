"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py . (Running without dependencies will also
result in error messages with download links.)
"""

from Manifest import DataSender
from Manifest import time, sys
from Manifest import CpuValue, NetworkValues

UPDATE_INTERVAL_SECS = 0.01

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'


STAT_SOURCES = {
	'CPU':		CpuValue.GetCpuValue,
	'NET_DOWN':	NetworkValues.GetDownloadValue,
	'NET_UP':	NetworkValues.GetUploadValue,
}


if __name__ == '__main__':
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		while True:
			stats = {}
			for keyName, getValueFn in STAT_SOURCES.iteritems():
				value = getValueFn()
				if value is not None:
					stats[keyName] = value
			for i, cpuValue in enumerate(CpuValue.GetCpuValues()):
				v = cpuValue/100.0
				stats['CPU%d' % i] = v
				break

			arduinoSerial.write(DataSender.Format(**stats))

			line = arduinoSerial.readline()
			while line:
				sys.stdout.write(line)
				sys.stdout.flush()
				line = arduinoSerial.readline()

			time.sleep(UPDATE_INTERVAL_SECS)

