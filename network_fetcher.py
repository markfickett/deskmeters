"""
Get network stats from the system and provide a value to drive analog display.
"""

__all__ = [
	'NetworkFetcher',
]

from Manifest import net_stat, auto_fetcher

class NetworkFetcher(auto_fetcher.AutoFetcher):
	def __init__(self, interval, smoothingWindow=10, **kwargs):
		auto_fetcher.AutoFetcher.__init__(self, interval, **kwargs)
		self.__upBytes = net_stat.GetSentBytes()
		self.__dnBytes = net_stat.GetReceivedBytes()
		self.__window = smoothingWindow
		self.__upBytesRates = [0,]*self.__window
		self.__dnBytesRates = list(self.__upBytesRates)
		self.__dt = interval

	def _update(self):
		self.__upBytes = self.__updateByteRate(self.__upBytesRates,
			self.__upBytes, net_stat.GetSentBytes())
		self.__dnBytes = self.__updateByteRate(self.__dnBytesRates,
			self.__dnBytes, net_stat.GetReceivedBytes())
		self._callChangeCallback()

	def __updateByteRate(self, ratesList, prevBytes, currentBytes):
		ratesList.pop()
		ratesList.insert(0, (currentBytes - prevBytes) / self.__dt)
		return currentBytes

	def getBps(self):
		"""
		@return an (upload, download) tuple of Bytes per second values,
			smoothed over the window
		"""
		return (sum(self.__upBytesRates)/self.__window,
			sum(self.__dnBytesRates)/self.__window)

	def getValues(self):
		"""
		@return an (upload, download) tuple mapped using
			BytesPerSecondToFloat
		"""
		return map(BytesPerSecondToFloat, self.getBps())


FLOAT_RANGE_INC = 0.2
FLOAT_RANGE_MAX = 1.0
BITS_RANGE = 1024
def BytesPerSecondToFloat(bytesPerSecond):
	"""
	Map throughput values to [0.0, 1.0] where
		throughput	maps to
		 bps [0, 1024)	[0.0, 0.2)
		kbps [1, 1024)	[0.2, 0.4)
		kBps [1, 1024)	[0.4, 0.6)
		MBps [1, 1024)	[0.6, 0.8)
		GBps [1, 1024]	[0.8, 1.0]
	"""
	floatBase = 0.0
	adjustedBps = bytesPerSecond * BITS_RANGE # start at bits per second
	while floatBase < FLOAT_RANGE_MAX:
		if adjustedBps < BITS_RANGE:
			return (floatBase +
				(adjustedBps/BITS_RANGE)*FLOAT_RANGE_INC)
		adjustedBps /= BITS_RANGE
		floatBase += FLOAT_RANGE_INC
	return FLOAT_RANGE_MAX


