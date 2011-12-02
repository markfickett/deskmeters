from Manifest import psutil

def GetRamUsedFraction():
	"""Get the decimal fraction in [0.0, 1.0] of used physical memory."""
	return psutil.used_phymem() / float(psutil.TOTAL_PHYMEM)

