import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

led_pin1 = 20
led_pin2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

pwm = GPIO.PWM(led_pin1, 1000)
pwm.start(0)

try:
    while True:
        for duty in range(0, 101, 5):
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
        
        for duty in range(100, -1, -5):
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("program killed")
    sys.exit(0)
