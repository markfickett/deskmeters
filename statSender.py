"""
Write various stats to Serial, for the Arduino which drives the LED strips
and the meters.

This depends on:
	psutil: http://code.google.com/p/psutil/
	pySerial: http://pyserial.sourceforge.net/
"""

import psutil
import serial
import sys

KEY_CPU = 'CPU'
SERIAL_DEVICE = '/dev/tty.usbmodemfd131'
SERIAL_BAUD = 9600

if __name__ == '__main__':
	arduinoSerial = serial.Serial(SERIAL_DEVICE, SERIAL_BAUD)
	while True:
		stats = {
			KEY_CPU: psutil.cpu_percent(),
		}
		arduinoSerial.write('\n'.join(
			['%s\t%s' % (label, value) for label, value
				in stats.iteritems()])
			)
		print '.',
		sys.stdout.flush()
	arduinoSerial.close()

