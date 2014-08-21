"""
Wrap netstat, to get total (and incremental) upload/download data counts.

The netstat expected behavior is something like:
$ netstat -s -p tcp
tcp:
  3803202 packets sent
    2997416 data packets (2644623460 bytes) # this taken for 'sent'
    3114 data packets (2723758 bytes) retransmitted
    [...]
  2704958 packets received
    1498594 acks (for 2644332881 bytes)
    46626 duplicate acks
    0 acks for unsent data
    1149258 packets (1383209139 bytes) received in-sequence # 'rec'
    [...]
"""

__all__ = [
  'GetSentBytes',
  'GetReceivedBytes',

  'BYTES_PER_KB',
  'BYTES_PER_MB',
  'BYTES_PER_GB',

  'Format',
]

from Manifest import subprocess, re

BYTES_PER_KB = 1024
BYTES_PER_MB = 1024*BYTES_PER_KB
BYTES_PER_GB = 1024*BYTES_PER_MB

_RE_BYTES_SENT = re.compile(r'^tcp:.*?packets sent.*?\((\d+) bytes\)$',
  re.DOTALL|re.MULTILINE)
_RE_BYTES_RECEIVED = re.compile(r'^tcp:.*?packets \((\d+) bytes\) received',
  re.DOTALL|re.MULTILINE)

def _GetNetstatText():
  """
  Get the statistics text output from netstat, for TCP.
  @return the generated text
  """
  return subprocess.check_output(['netstat', '-s', '-p', 'tcp'])

def _GetNetstatValue(byteRegexp):
  """
  Get a byte value from netstat's statistics output.
  @param byteRegexp: a regular expression which, when applied to netstat's
    output, produces a byte value
  @return an integer byte value from netstat's statistics
  """
  text = _GetNetstatText()
  return int(byteRegexp.search(text).group(1))

def GetSentBytes():
  return _GetNetstatValue(_RE_BYTES_SENT)

def GetReceivedBytes():
  return _GetNetstatValue(_RE_BYTES_RECEIVED)


_UNITS = (
  (BYTES_PER_GB, 'GB'),
  (BYTES_PER_MB, 'MB'),
  (BYTES_PER_KB, 'KB'),
  (1, 'B'),
)
def Format(byte_count, suffix=''):
  if byte_count < 1:
    return str(byte_count)
  for unit_count, name in _UNITS:
    if byte_count >= unit_count:
      converted = float(byte_count) / unit_count
      return '%.2f %s%s' % (converted, name, suffix)


if __name__ == '__main__':
  import time

  dt = 0.25
  last_bytes_pair = (GetSentBytes(), GetReceivedBytes())
  while True:
    current_bytes_pair = (GetSentBytes(), GetReceivedBytes())
    d_bytes_pair = [current_bytes - last_bytes
      for current_bytes, last_bytes
      in zip(current_bytes_pair, last_bytes_pair)]
    bps_pair = [Format(d_bytes/dt, 'ps') for d_bytes in d_bytes_pair]
    print ('Up: %10s\tDown: %10s' % tuple(bps_pair))
    last_bytes_pair = current_bytes_pair

    time.sleep(dt)
