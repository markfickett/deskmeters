from Manifest import auto_fetcher, mcstatus

class MinecraftFetcher(auto_fetcher.AutoFetcher):
	"""Get the number of online players in a Minecraft server."""
	def __init__(self, interval, changeCallback, host):
		auto_fetcher.AutoFetcher.__init__(
			self,
			interval, changeCallback)
		self.__server = mcstatus.McServer(host)
		self.__n = 0

	def _update(self):
		changed = False
		with self._lockGuard():
			self.__server.Update()
			n = self.__server.num_players_online
			if n != self.__n:
				changed = True
				self.__n = n
		if changed:
			self._callChangeCallback()

	def getNumPlayersOnline(self):
		with self._lockGuard():
			return self.__n


