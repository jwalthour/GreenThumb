print("importing")
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 # sudo pip install adafruit-ads1x15

print("GPIO setup")
GPIO.setmode(GPIO.BOARD)
ADC_PIN_NUM = 7
SENSE_PIN_0 = 13
SENSE_PIN_1 = 29
GPIO.setup([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1], GPIO.OUT)

# Power on sensor and ADC
print("Connecting to ADC")
GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.HIGH)
adc = Adafruit_ADS1x15.ADS1015(0x48)
print("0,1")
try:
	while True:
		print(str(adc.read_adc(0)) + "," + str(adc.read_adc(1)))
		GPIO.output(SENSE_PIN_0,GPIO.LOW)
		GPIO.output(SENSE_PIN_1,GPIO.LOW)
		time.sleep(1)
		GPIO.output(SENSE_PIN_0,GPIO.HIGH)
		GPIO.output(SENSE_PIN_1,GPIO.HIGH)
finally:
	print("Powering down sensor and ADC.")
	GPIO.output([ADC_PIN_NUM,SENSE_PIN_0,SENSE_PIN_1],GPIO.LOW)

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpowered.
	#GPIO.cleanup()
