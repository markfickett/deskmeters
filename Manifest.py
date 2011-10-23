"""
Centralize all the imports for deskmeters' Python (PC) side.
"""

import time, subprocess, re

try:
	import psutil
except ImportError, e:
	print 'Required: psutil from http://code.google.com/p/psutil/'
	raise e

try:
	import serial
except ImportError, e:
	print 'Required: pySerial from http://pyserial.sourceforge.net/'
	raise e

import NetStat, CpuValue, NetworkValues

