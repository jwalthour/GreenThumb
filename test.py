import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # sudo pip install adafruit-ads1x15

GPIO.setmode(GPIO.BOARD)
adc_pin = 7
sens_pin = 13
GPIO.setup([adc_pin,sens_pin], GPIO.OUT)

# Power on sensor and ADC
GPIO.output([adc_pin,sens_pin],GPIO.HIGH)
adc = Adafruit_ADS1x15.ADS1015(0x48)
try:
	while True:
		print("Got sensor value: " + str(adc.read_adc(0)))
		time.sleep(0.2)
finally:
	print("Powering down sensor and ADC.")
	GPIO.output([adc_pin,sens_pin],GPIO.LOW)

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpowered.
	#GPIO.cleanup()
