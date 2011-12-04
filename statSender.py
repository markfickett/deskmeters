"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py . (Running without dependencies will also
result in error messages with download links.)
"""

from Manifest import DataSender
from Manifest import time, sys
from Manifest import CpuFetcher, NetworkFetcher, RamFetcher
from Manifest import threading, AutoFetcher

UPDATE_INTERVAL_SECS =		1.0
UPDATE_INTERVAL_SECS_CPU =	0.1
UPDATE_INTERVAL_SECS_RAM =	0.5
UPDATE_INTERVAL_SECS_NET =	1.0

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'


class ThreadSafeSender:
	"""
	Provide a thread-safe method to send data to the Arduino.
	"""
	def __init__(self, arduinoSerial):
		self.__arduinoSerial = arduinoSerial
		self.__lock = threading.Lock()

	def send(self, **kwargs):
		with AutoFetcher.LockGuard(self.__lock):
			self.__arduinoSerial.write(DataSender.Format(**kwargs))


if __name__ == '__main__':
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		DataSender.WaitForReady(arduinoSerial)

		sender = ThreadSafeSender(arduinoSerial)

		def cpuChangedCallback(fetcher):
			ave = fetcher.getAverage()
			stats = {
				'CPU': ave,
				'CPU_INT': CpuFetcher.FractionToInterval(ave),
			}
			for i, cpuValue in enumerate(fetcher.getValues()):
				stats['CPU%d' % (i+1)] = cpuValue
			sender.send(**stats)

		def ramChangedCallback(fetcher):
			sender.send(RAM=fetcher.getFraction())

		def netChangedCallback(fetcher):
			netUp, netDown = fetcher.getValues()
			sender.send(NET_UP=netUp, NET_DOWN=netDown)

		fetchers = (
			CpuFetcher.CpuFetcher(UPDATE_INTERVAL_SECS_CPU,
				changeCallback=cpuChangedCallback),
			RamFetcher.RamFetcher(UPDATE_INTERVAL_SECS_RAM,
				changeCallback=ramChangedCallback),
			NetworkFetcher.NetworkFetcher(UPDATE_INTERVAL_SECS_NET,
				changeCallback=netChangedCallback),
		)

		while any(map(lambda fetcher: fetcher.isAlive(), fetchers)):
			try:
				line = arduinoSerial.readline()
				while line:
					sys.stdout.write(line)
					sys.stdout.flush()
					line = arduinoSerial.readline()

				time.sleep(UPDATE_INTERVAL_SECS)
			except KeyboardInterrupt, e:
				print 'Killed, exiting.'
				break

