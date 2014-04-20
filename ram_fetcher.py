from Manifest import psutil, auto_fetcher

class RamFetcher(auto_fetcher.AutoFetcher):
	"""
	Get the decimal fraction in [0.0, 1.0] of used physical memory.
	"""
	def _update(self):
		with self._lockGuard():
			self.__fraction = (psutil.used_phymem()
				/ float(psutil.TOTAL_PHYMEM))
		self._callChangeCallback()

	def getFraction(self):
		with self._lockGuard():
			return self.__fraction


