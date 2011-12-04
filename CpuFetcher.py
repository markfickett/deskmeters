"""
Get CPU stats from the system and provide a value to drive analog display.
"""

__all__ = [
	'CpuFetcher',
	'DecimalToInterval',
]

from Manifest import AutoFetcher, psutil

class CpuFetcher(AutoFetcher.AutoFetcher):
	"""
	Automatically track and update a rolling window of CPU usage numbers.
	Provide an overall average and per-core values, as [0.0, 1.0] values.
	"""
	def __init__(self, interval, smoothingWindow=8, **kwargs):
		AutoFetcher.AutoFetcher.__init__(self, interval, **kwargs)
		self.__window = smoothingWindow

		self.__ave = 0.0
		self.__values = {}
		numCpus = len(psutil.cpu_percent(percpu=True))
		empty = [0.0,]*self.__window
		for key in range(numCpus):
			self.__values[key] = list(empty)

	def _update(self):
		# per-core list of [0, 100] values
		perCpu = psutil.cpu_percent(percpu=True)
		sumOfAverages = 0.0
		with self._lockGuard():
			for i, decPercent in enumerate(perCpu):
				# Add the new value, drop the oldest.
				values = self.__values[i][1:]
				values.append(decPercent/100.0)
				self.__values[i] = values
				sumOfAverages += sum(values)/self.__window
			self.__ave = sumOfAverages/len(self.__values)
		self._callChangeCallback()

	def getSingle(self, i):
		"""
		@return the [0.0, 1.0] usage value for the specified CPU,
			smoothed over the fetcher's window
		"""
		with self._lockGuard():
			return sum(self.__values[i])/self.__window

	def getAverage(self):
		"""
		@return the [0.0, 1.0] average usage value for all CPUs,
			smoothed over the fetcher's window
		"""
		with self._lockGuard():
			return self.__ave

	def getValues(self):
		"""
		@return a list, in order, of the [0.0, 1.0] usage values for
			all the CPUs, each smoothed over the fetcher's window
		"""
		with self._lockGuard():
			for singleCpuValues in self.__values.values():
				yield sum(singleCpuValues)/self.__window


INTERVAL_MAX = 300
INTERVAL_MIN = 20

def FractionToInterval(cpuValue):
	"""
	Get the update interval (1/speed) for the lights representing CPU usage.
	"""
	return int(-(INTERVAL_MAX-INTERVAL_MIN)*cpuValue**2 + INTERVAL_MAX)

