"""
Get CPU stats from the system and provide a value to drive analog display.
"""

__all__ = [
	'GetCpuValue',
]

from Manifest import psutil

UPDATE_WINDOW = 8

CPU_MARQUEE_INTERVAL_MAX = 300

CpuValues = None

def GetCpuValue():
	"""
	Get the update interval (1/speed) for the lights representing CPU usage.
	Average over the last UPDATE_WINDOW values.
	"""
	global CpuValues
	if CpuValues is None:
		CpuValues = [0.0,]*UPDATE_WINDOW
	CpuValues = CpuValues[1:]
	CpuValues.append(psutil.cpu_percent())

	cpuAverage = sum(CpuValues)/len(CpuValues)
	scaleFactor = (1.0 - cpuAverage/100.0)**3
	return int(scaleFactor*CPU_MARQUEE_INTERVAL_MAX)


