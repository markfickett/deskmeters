"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py . (Running without dependencies will also
result in error messages with download links.)
"""

from Manifest import DataSender
from Manifest import time
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

			arduinoSerial.write(DataSender.Format(**stats))

			lines = ''
			line = arduinoSerial.readline()
			while line:
				lines += line
				line = arduinoSerial.readline()
			if lines:
				print lines

			time.sleep(UPDATE_INTERVAL_SECS)

