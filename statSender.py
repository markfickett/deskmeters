"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py . (Running without dependencies will also
result in error messages with download links.)
"""

from Manifest import DataSender
from Manifest import time, sys
from Manifest import CpuFetcher, NetworkValues, RamValues

UPDATE_INTERVAL_SECS = 0.1

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'


STAT_SOURCES = {
	'NET_DOWN':	NetworkValues.GetDownloadValue,
	'NET_UP':	NetworkValues.GetUploadValue,
	'RAM':		RamValues.GetRamUsedFraction,
}


if __name__ == '__main__':
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		time.sleep(2.0) # TODO send a 'ready' instead
		cpuFetcher = CpuFetcher.CpuFetcher(UPDATE_INTERVAL_SECS)
		while True:
			stats = {}
			for keyName, getValueFn in STAT_SOURCES.iteritems():
				value = getValueFn()
				if value is not None:
					stats[keyName] = value

			# TODO: auto-send, don't poll, since fetcher updates
			stats['CPU'] = CpuFetcher.DecimalToInterval(
				cpuFetcher.getAverage())
			for i, cpuValue in enumerate(cpuFetcher.getValues()):
				stats['CPU%d' % (i+1)] = cpuValue

			arduinoSerial.write(DataSender.Format(**stats))

			line = arduinoSerial.readline()
			while line:
				sys.stdout.write(line)
				sys.stdout.flush()
				line = arduinoSerial.readline()

			time.sleep(UPDATE_INTERVAL_SECS)

