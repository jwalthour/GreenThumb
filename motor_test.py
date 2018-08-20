import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
pin_ena = 22
pin_in1 = 16
pin_in2 = 18
GPIO.setup([pin_ena,
			pin_in1,
			pin_in2], GPIO.OUT)
GPIO.output([pin_ena,
			pin_in1,
			pin_in2], GPIO.LOW)

try:
	print("Dir 1")
	# Doesn't do anything with my pump.
	GPIO.output(pin_in1, GPIO.LOW)
	GPIO.output(pin_in2, GPIO.HIGH)
	GPIO.output(pin_ena, GPIO.HIGH)
	time.sleep(5)
	print("Dir 2")
	GPIO.output(pin_in1, GPIO.HIGH)
	GPIO.output(pin_in2, GPIO.LOW)
	time.sleep(5)
	GPIO.output(pin_ena, GPIO.LOW)
finally:
	print("Stopping motor.")
	GPIO.output([pin_ena,
				pin_in1,
				pin_in2], GPIO.LOW)

	# Explicitly do not cleanup.  This leaves the pins low, and thus the devices unpower$
	#GPIO.cleanup()


