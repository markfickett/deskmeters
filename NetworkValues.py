"""
Get network stats from the system and provide a value to drive analog display.
"""

__all__ = [
	'GetDownloadValue',
	'GetUploadValue',
]

from Manifest import NetStat

# Send a spot every NET_DOWN_CHUNK bytes.
NET_DOWN_CHUNK = NetStat.BYTES_PER_KB * 100
NET_UP_CHUNK = NetStat.BYTES_PER_KB * 10

def _GetValue(prevBytes, getBytesFn, chunkSize):
	"""
	@return adjustedPrevBytes, outputValue
	"""
	currentBytes = getBytesFn()
	dBytes = currentBytes - prevBytes
	numChunks = dBytes / chunkSize
	if numChunks > 0:
		prevBytes += numChunks*chunkSize
		intensity = 1.0 - 0.5**numChunks
		outputValue = intensity
	else:
		outputValue = None
	return prevBytes, outputValue


PreviousRecBytes = NetStat.GetReceivedBytes()
def GetDownloadValue():
	"""
	Calculate a number based on the number of bytes downloaded since last
	report. Return an intensity in [0, 1.0] that is greater for more data.
	Chunk reports (so a consistent low bandwidth download will produce
	occasional pulses, not constant dim skitter).
	@return an intensity for a pulse to show, or None for no pulse
	"""
	global PreviousRecBytes
	PreviousRecBytes, outputValue = _GetValue(
		PreviousRecBytes, NetStat.GetReceivedBytes, NET_DOWN_CHUNK)
	return outputValue


PreviousSentBytes = NetStat.GetSentBytes()
def GetUploadValue():
	"""
	@see GetDownloadValue
	"""
	global PreviousSentBytes
	PreviousSentBytes, outputValue = _GetValue(
		PreviousSentBytes, NetStat.GetSentBytes, NET_UP_CHUNK)
	return outputValue


