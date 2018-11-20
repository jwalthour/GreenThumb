"""
Check the moisture sensors exactly once.  Log to file.  If sensor 0 reports moisture below
threshold, dispense water for a fixed amount of time.
"""

print("importing")
import datetime 
import time
import os.path
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # sudo pip install adafruit-ads1x15

print("GPIO setup")
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

LOGFILE='/home/gardener/watering_log.csv'
print("Opening log file")
existed_already = os.path.isfile(LOGFILE)
logfile = open(LOGFILE, 'a')
if not existed_already:
	# This is our first time opening the file; print CSV header
	logfile.write('time,"ADC0","ADC1","moisture 0","moisture 1","watered?"\r\n')

# Power on sensor and ADC
print("Connecting to ADC")
GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.HIGH)
adc = Adafruit_ADS1x15.ADS1015(0x48)

# Value, in ADC ticks, corresponding to saturated soil
# ADC_WETTEST_READING=1340.0
ADC_WETTEST_READING=1
# Moisture fraction at which water is dispensed
WATERING_THRESHOLD_FRAC = 0.75
# The number of seconds for which the pump should be run in one watering.
WATERING_PUMP_DURATION_S = 1.5


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
	log_line = datetime.datetime.now().strftime('"%Y-%m-%d %H:%M:%S",')
	moistures_ticks = [adc.read_adc(chan) for chan in [0,1]]
	log_line += str(moistures_ticks[0]) + ',' + str(moistures_ticks[1]) + ','
	moistures_frac = [(m / ADC_WETTEST_READING) for m in moistures_ticks]
	log_line += str(moistures_frac[0]) + ',' + str(moistures_frac[1]) + ','
	water = moistures_frac[0] < WATERING_THRESHOLD_FRAC
	log_line += str(water) + ','
	log_line += '\r\n'
	# Log and flush prior to running the motor, in case something happens during that.
	logfile.write(log_line)
	logfile.close()
	logfile = None
	if water:
		dispense_water()
finally:
	print("Powering down sensor and ADC.")
	GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)
	if logfile:
		logfile.close()

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpowered.
	#GPIO.cleanup()
