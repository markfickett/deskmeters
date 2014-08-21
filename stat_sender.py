"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

Dependencies are noted in Manifest.py . (Running without dependencies will also
result in error messages with download links.)
"""

from Manifest import data_sender
from Manifest import time, sys
from Manifest import cpu_fetcher, network_fetcher, ram_fetcher
from Manifest import minecraft_fetcher
from Manifest import threading, auto_fetcher

from Manifest import ledcontroller
from ledcontroller.Manifest import SendingBuffer, SendingPatternList, sequences
from ledcontroller.patterns.Manifest import InterpolatedMarquee

UPDATE_INTERVAL_SECS = 1.0
UPDATE_INTERVAL_SECS_CPU = 0.1
UPDATE_INTERVAL_SECS_RAM = 0.5
UPDATE_INTERVAL_SECS_NET = 1.0
UPDATE_INTERVAL_SECS_MC = 5.0

MINECRAFT_HOST = # 'my.minecraft.server.com'
MINECRAFT_MAX_DISPLAYABLE_PLAYERS = 10.0

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'


class ThreadSafeSender:
  """
  Provide a thread-safe method to send data to the Arduino.
  """
  def __init__(self, arduino_serial):
    self.__arduino_serial = arduino_serial
    self.__lock = threading.Lock()

  def Send(self, **kwargs):
    with self.__lock:
      self.__arduino_serial.write(data_sender.Format(**kwargs))


if __name__ == '__main__':
  with data_sender.SerialGuard(SERIAL_DEVICE) as arduino_serial:
    data_sender.WaitForReady(arduino_serial)

    sender = ThreadSafeSender(arduino_serial)

    color_sender = SendingPatternList(sending_buffer=SendingBuffer(sender))
    marquee = InterpolatedMarquee(sequences.GenerateHueGradient())
    color_sender.Append(marquee)

    def CpuChangedCallback(fetcher):
      ave = fetcher.GetAverage()
      marquee.SetSpeed(ave * 10)
      per_cpu_stats = {}
      for i, cpu_value in enumerate(fetcher.GetValues()):
        per_cpu_stats['CPU%d' % (i+1)] = cpu_value
      sender.Send(**per_cpu_stats)
      color_sender.UpdateAndSend()

    def RamChangedCallback(fetcher):
      sender.Send(RAM=fetcher.GetFraction())

    def NetChangedCallback(fetcher):
      netUp, netDown = fetcher.GetValues()
      sender.Send(NET_UP=netUp, NET_DOWN=netDown)

    def MinecraftChangedCallback(fetcher):
      display_num = (fetcher.GetNumPlayersOnline() /
        MINECRAFT_MAX_DISPLAYABLE_PLAYERS)
      sender.Send(MINECRAFT=display_num)

    fetchers = (
      cpu_fetcher.CpuFetcher(UPDATE_INTERVAL_SECS_CPU,
        change_callback=CpuChangedCallback),
      ram_fetcher.RamFetcher(UPDATE_INTERVAL_SECS_RAM,
        change_callback=RamChangedCallback),
      network_fetcher.NetworkFetcher(UPDATE_INTERVAL_SECS_NET,
        change_callback=NetChangedCallback),
      minecraft_fetcher.MinecraftFetcher(
        UPDATE_INTERVAL_SECS_MC,
        MinecraftChangedCallback,
        MINECRAFT_HOST)
    )

    while any(map(lambda fetcher: fetcher.IsAlive(), fetchers)):
      try:
        line = arduino_serial.readline()
        while line:
          sys.stdout.write(line)
          sys.stdout.flush()
          line = arduino_serial.readline()

        time.sleep(UPDATE_INTERVAL_SECS)
      except KeyboardInterrupt, e:
        print 'Killed, exiting.'
        break
