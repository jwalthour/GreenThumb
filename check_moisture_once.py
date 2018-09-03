"""
Check the moisture sensors exactly once and log to a file.

The idea here is to put a call to this in crontab, so it gets called periodically.
"""

print("importing")
import datetime 
import os.path
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # sudo pip install adafruit-ads1x15

print("GPIO setup")
GPIO.setmode(GPIO.BOARD)
ADC_PIN_NUM = 7
SENSE_PIN_0 = 13
SENSE_PIN_1 = 29
GPIO.setup([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1], GPIO.OUT)

LOGFILE='/home/gardener/moisture_log.csv'
print("Opening log file")
existed_already = os.path.isfile(LOGFILE)
logfile = open(LOGFILE, 'a')
if not existed_already:
	# This is our first time opening the file; print CSV header
	logfile.write("time,0,1\r\n")

# Power on sensor and ADC
print("Connecting to ADC")
GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.HIGH)
adc = Adafruit_ADS1x15.ADS1015(0x48)

# Value, in ADC ticks, corresponding to saturated soil
ADC_WETTEST_READING=1340

try:
	line = datetime.datetime.now().strftime('"%Y-%m-%d %H:%M:%S",')
	line += str(adc.read_adc(0)) + "," + str(adc.read_adc(1))
	line += '\r\n'
	logfile.write(line)
finally:
	print("Powering down sensor and ADC.")
	GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpowered.
	#GPIO.cleanup()
