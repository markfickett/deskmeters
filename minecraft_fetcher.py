from Manifest import auto_fetcher, mcstatus

class MinecraftFetcher(auto_fetcher.AutoFetcher):
  """Get the number of online players in a Minecraft server."""
  def __init__(self, interval, change_callback, host):
    auto_fetcher.AutoFetcher.__init__(
      self,
      interval, change_callback)
    self.__server = mcstatus.McServer(host)
    self.__n = 0

  def _Update(self):
    changed = False
    with self._LockGuard():
      self.__server.Update()
      n = self.__server.num_players_online
      if n != self.__n:
        changed = True
        self.__n = n
    if changed:
      self._CallChangeCallback()

  def GetNumPlayersOnline(self):
    with self._lockGuard():
      return self.__n
