from Manifest import psutil, auto_fetcher

class RamFetcher(auto_fetcher.AutoFetcher):
  """
  Get the decimal fraction in [0.0, 1.0] of used physical memory.
  """
  def _Update(self):
    with self._LockGuard():
      self.__fraction = (psutil.used_phymem()
        / float(psutil.TOTAL_PHYMEM))
    self._CallChangeCallback()

  def GetFraction(self):
    with self._LockGuard():
      return self.__fraction
