"""
Get network stats from the system and provide a value to drive analog display.
"""

__all__ = [
  'NetworkFetcher',
]

from Manifest import net_stat, auto_fetcher

class NetworkFetcher(auto_fetcher.AutoFetcher):
  def __init__(self, interval, smoothing_window=10, **kwargs):
    auto_fetcher.AutoFetcher.__init__(self, interval, **kwargs)
    self.__up_bytes = net_stat.GetSentBytes()
    self.__dn_bytes = net_stat.GetReceivedBytes()
    self.__window = smoothing_window
    self.__up_bytes_rates = [0,] * self.__window
    self.__dn_bytes_rates = list(self.__up_bytes_rates)
    self.__dt = interval

  def _Update(self):
    self.__up_bytes = self.__UpdateByteRate(self.__up_bytes_rates,
      self.__up_bytes, net_stat.GetSentBytes())
    self.__dn_bytes = self.__UpdateByteRate(self.__dn_bytes_rates,
      self.__dn_bytes, net_stat.GetReceivedBytes())
    self._CallChangeCallback()

  def __UpdateByteRate(self, rates_list, prev_bytes, current_bytes):
    rates_list.pop()
    rates_list.insert(0, (current_bytes - prev_bytes) / self.__dt)
    return current_bytes

  def GetBps(self):
    """
    @return an (upload, download) tuple of Bytes per second values,
      smoothed over the window
    """
    return (sum(self.__up_bytes_rates) / self.__window,
      sum(self.__dn_bytes_rates) / self.__window)

  def GetValues(self):
    """
    @return an (upload, download) tuple mapped using
      BytesPerSecondToFloat
    """
    return map(BytesPerSecondToFloat, self.GetBps())


FLOAT_RANGE_INC = 0.2
FLOAT_RANGE_MAX = 1.0
BITS_RANGE = 1024
def BytesPerSecondToFloat(bytes_per_second):
  """
  Map throughput values to [0.0, 1.0] where
    throughput  maps to
     bps [0, 1024)  [0.0, 0.2)
    kbps [1, 1024)  [0.2, 0.4)
    kBps [1, 1024)  [0.4, 0.6)
    MBps [1, 1024)  [0.6, 0.8)
    GBps [1, 1024]  [0.8, 1.0]
  """
  float_base = 0.0
  adjusted_bps = bytes_per_second * BITS_RANGE # start at bits per second
  while float_base < FLOAT_RANGE_MAX:
    if adjusted_bps < BITS_RANGE:
      return (float_base +
        (adjusted_bps/BITS_RANGE)*FLOAT_RANGE_INC)
    adjusted_bps /= BITS_RANGE
    float_base += FLOAT_RANGE_INC
  return FLOAT_RANGE_MAX
