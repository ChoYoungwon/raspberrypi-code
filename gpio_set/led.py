import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.OUT)

state = "off"

while True:
	try:
		GPIO.output(20, True)
		if GPIO.input(16) == 0:
			if state == "on":
				print("off")
				state = "off"
			time.sleep(0.5)
   
		elif GPIO.input(16) == 1:			
			if state == "off":
				print("on")
				state = "on"
			time.sleep(0.1)

		GPIO.output(20, False)

		if GPIO.input(16) == 0:
			time.sleep(0.5)
		else:
			time.sleep(0.1)
		
	except KeyboardInterrupt:
		print("program killed")
		sys.exit()
