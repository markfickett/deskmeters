"""
Get CPU stats from the system and provide a value to drive analog display.
"""

__all__ = [
  'CpuFetcher',
  'DecimalToInterval',
]

from Manifest import auto_fetcher, psutil

class CpuFetcher(auto_fetcher.AutoFetcher):
  """
  Automatically track and update a rolling window of CPU usage numbers.
  Provide an overall average and per-core values, as [0.0, 1.0] values.
  """
  def __init__(self, interval, smoothing_window=8, **kwargs):
    auto_fetcher.AutoFetcher.__init__(self, interval, **kwargs)
    self.__window = smoothing_window

    self.__ave = 0.0
    self.__values = {}
    num_cpus = len(psutil.cpu_percent(percpu=True))
    empty = [0.0,] * self.__window
    for key in range(num_cpus):
      self.__values[key] = list(empty)

  def _Update(self):
    # per-core list of [0, 100] values
    per_cpu = psutil.cpu_percent(percpu=True)
    sum_of_averages = 0.0
    with self._LockGuard():
      for i, dec_percent in enumerate(per_cpu):
        # Add the new value, drop the oldest.
        values = self.__values[i][1:]
        values.append(dec_percent/100.0)
        self.__values[i] = values
        sum_of_averages += sum(values)/self.__window
      self.__ave = sum_of_averages/len(self.__values)
    self._CallChangeCallback()

  def GetSingle(self, i):
    """
    @return the [0.0, 1.0] usage value for the specified CPU,
      smoothed over the fetcher's window
    """
    with self._LockGuard():
      return sum(self.__values[i]) / self.__window

  def GetAverage(self):
    """
    @return the [0.0, 1.0] average usage value for all CPUs,
      smoothed over the fetcher's window
    """
    with self._LockGuard():
      return self.__ave

  def GetValues(self):
    """
    @return a list, in order, of the [0.0, 1.0] usage values for
      all the CPUs, each smoothed over the fetcher's window
    """
    with self._LockGuard():
      for single_cpu_values in self.__values.values():
        yield sum(single_cpu_values) / self.__window


INTERVAL_MAX = 300
INTERVAL_MIN = 20

def FractionToInterval(cpu_value):
  """
  Get the update interval (1/speed) for the lights representing CPU usage.
  """
  return int(-(INTERVAL_MAX-INTERVAL_MIN) * cpu_value**2 + INTERVAL_MAX)

