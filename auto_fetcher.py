__all__ = [
  'AutoFetcher',
]

from Manifest import threading, time


class AutoFetcher:
  def __init__(self, interval, change_callback=None):
    self.__thread = threading.Thread(target=self.__UpdateForever)
    self.__interval = max(0, float(interval))
    self.__thread.daemon = True
    self.__thread.start()
    self.__lock = threading.Lock()
    self.__change_callback = change_callback

  def _LockGuard(self):
    return self.__lock

  def __UpdateForever(self):
    while True:
      time.sleep(self.__interval)
      self._Update()

  def _Update(self):
    raise NotImplementedError()

  def _CallChangeCallback(self):
    if self.__change_callback:
      try:
        self.__change_callback(self)
      except Exception, e:
        print ('Error calling %s: %s'
          % (self.__change_callback, e))
        self.__change_callback = None

  def IsAlive(self):
    return self.__thread.isAlive()
