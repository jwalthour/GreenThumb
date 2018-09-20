"""
Check the moisture sensors exactly once.  Log to file.  If sensor 0 reports moisture below
threshold, dispense water for a fixed amount of time.
"""

from __future__ import print_function
print("Importing... ", end='')
import datetime 
import time
import os.path
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # sudo pip install adafruit-ads1x15
print("done.")

print("GPIO setup... ", end='')
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ADC_PIN_NUM = 7
SENSE_PIN_0 = 13
SENSE_PIN_1 = 29
PIN_ENA = 22
PIN_IN1 = 16
PIN_IN2 = 18
GPIO.setup([PIN_ENA,
			PIN_IN1,
			PIN_IN2], GPIO.OUT)
GPIO.output([PIN_ENA,
			PIN_IN1,
			PIN_IN2], GPIO.LOW)

GPIO.setup([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1], GPIO.OUT)
print("done.")

LOGFILE='/home/gardener/watering_log.csv'
print("Opening log file... ", end='')
existed_already = os.path.isfile(LOGFILE)
logfile = open(LOGFILE, 'a')
if not existed_already:
	# This is our first time opening the file; print CSV header
	logfile.write('time,"ADC0","ADC1","moisture 0","moisture 1","watered?"\r\n')
print("done.")

# Power on sensor and ADC
print("Connecting to ADC... ", end='')
GPIO.output([ADC_PIN_NUM],GPIO.HIGH)
adc = Adafruit_ADS1x15.ADS1015(0x48)
print("done.")


# Value, in ADC ticks, corresponding to saturated soil
ADC_WETTEST_READING=1340.0
# Moisture fraction at which water is dispensed
WATERING_THRESHOLD_FRAC = 0.75
# The number of seconds for which the pump should be run in one watering.
WATERING_PUMP_DURATION_S = 1.5

# Number of times to sample the sensor
NUM_SAMPLES = 500
SAMPLE_INTERVAL_S = 0.1

def dispense_water():
	try:
		# Set motor direction
		GPIO.output(PIN_IN1, GPIO.HIGH)
		GPIO.output(PIN_IN2, GPIO.LOW)
		# Enable motor
		GPIO.output(PIN_ENA, GPIO.HIGH)
		# Let the motor run
		time.sleep(WATERING_PUMP_DURATION_S)
	finally:
		# Disable motor
		GPIO.output([PIN_ENA,
					PIN_IN1,
					PIN_IN2], GPIO.LOW)
		

try:
	print("Taking readings... ", end='')
	water = False
	accum_moisture = 0;
	for i in range(0, NUM_SAMPLES):
		log_line = datetime.datetime.now().strftime('"%Y-%m-%d %H:%M:%S.%f",')
		GPIO.output([SENSE_PIN_0,SENSE_PIN_1],GPIO.HIGH)
		moistures_ticks = [adc.read_adc(chan) for chan in [0,1]]
		GPIO.output([SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)
		log_line += str(moistures_ticks[0]) + ',' + str(moistures_ticks[1]) + ','
		moistures_frac = [(m / ADC_WETTEST_READING) for m in moistures_ticks]
		log_line += str(moistures_frac[0]) + ',' + str(moistures_frac[1]) + ','
		# water = moistures_frac[0] < WATERING_THRESHOLD_FRAC
		# log_line += str(water) + ','
		log_line += '\r\n'
		# print(log_line)
		logfile.write(log_line)
		time.sleep(SAMPLE_INTERVAL_S);
	# Log and flush prior to running the motor, in case something happens during that.
	logfile.close()
	logfile = None
	print("done.")

	if water:
		dispense_water()
finally:
	# print("Powering down sensor and ADC.")
	# GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)
	print("Powering down sensors.")
	GPIO.output([SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)
	if logfile:
		logfile.close()

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpowered.
	#GPIO.cleanup()
