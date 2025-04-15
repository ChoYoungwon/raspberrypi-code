import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 20
ECHO = 21
LED = 19
print("초음파 거리 측정기")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(TRIG, False)
print("초음파 출력 초기화")
time.sleep(2)

try:
    while True:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO) == 0:
            start = time.time()
            
        while GPIO.input(ECHO) == 1:
            stop = time.time()
            
        check_time = stop - start
        distance = check_time * 34300 / 2

        if distance >= 30.0:
            freq = 0.5
            print("Distance : %.1f cm, and freq : %.1fHz" % (distance, freq))
            period = 1 / freq
            period /= 2
            GPIO.output(LED, True)
            time.sleep(period)
            GPIO.output(LED, False)
            time.sleep(period)
        elif distance < 30.0 and distance >= 20.0:
            freq = 1
            print("Distance : %.1f cm, and freq : %.1fHz" % (distance, freq))
            period = 1 / freq
            period /= 2
            GPIO.output(LED, True)
            time.sleep(period)
            GPIO.output(LED, False)
            time.sleep(period)
        elif distance < 20 and distance >= 10:
            freq = 3
            print("Distance : %.1f cm, and freq : %.1fHz" % (distance, freq))
            period = 1 / freq
            period /= 2
            GPIO.output(LED, True)
            time.sleep(period)
            GPIO.output(LED, False)
            time.sleep(period)
        else:
            freq = 5
            print(f"Distance : %.1f cm, and freq : %.1fHz" % (distance, freq))
            period = 1 / freq
            period /= 2
            GPIO.output(LED, True)
            time.sleep(period)
            GPIO.output(LED, False)
            time.sleep(period)
        
except KeyboardInterrupt:
    print("거리 측정 완료")
    GPIO.cleanup()

