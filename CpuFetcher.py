"""
Get CPU stats from the system and provide a value to drive analog display.
"""

__all__ = [
	'CpuFetcher',
	'DecimalToInterval',
]

from Manifest import AutoFetcher, psutil

class CpuFetcher(AutoFetcher):
	def __init__(self, interval, smoothingWindow=8):
		AutoFetcher.__init__(self, interval)
		self.__window = smoothingWindow

		self.__ave = 0.0
		self.__values = {}
		numCpus = len(psutil.cpu_percent(percpu=True))
		empty = [0.0,]*self.__window
		for key in range(numCpus):
			self.__values[key] = list(empty)

	def _update(self):
		perCpu = psutil.cpu_percent(percpu=True)
		sumOfAverages = 0.0
		for k, v in enumerate(perCpu):
			values = self.__values[k][1:]
			values.append(v/100.0)
			self.__values[k] = values
			sumOfAverages += sum(values)
		self.__ave = sumOfAverages/len(self.__values)

	def getSingle(self, i):
		with self._lockGuard():
			return sum(self.__values[i])/self.__window

	def getAverage(self):
		with self._lockGuard():
			return self.__ave

	def getValues(self):
		with self._lockGuard():
			for singleCpuValues in self.__values.values():
				yield sum(singleCpuValues)/self.__window


CPU_MARQUEE_INTERVAL_MAX = 300

def DecimalToInterval(cpuValue):
	"""
	Get the update interval (1/speed) for the lights representing CPU usage.
	"""
	scaleFactor = (1.0 - cpuValue/100.0)**3
	return int(scaleFactor*CPU_MARQUEE_INTERVAL_MAX)

