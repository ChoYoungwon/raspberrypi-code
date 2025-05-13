import sys
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)

led_pin1 = 20
led_pin2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

pwm1 = GPIO.PWM(led_pin1, 1000)
pwm1.start(0)

pwm2 = GPIO.PWM(led_pin2, 1000)
pwm2.start(0)

# 깜빡이는 동작을 제어하기 위한 전역 변수
blink_active = False

# 깜빡이는 기능을 백그라운드에서 실행할 함수
def blink_leds():
    global blink_active
    while blink_active:
        pwm1.ChangeDutyCycle(100)
        pwm2.ChangeDutyCycle(30)
        time.sleep(0.2)
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        time.sleep(0.2)

try:
    blink_thread = None
    
    while True:
        a = input("0~4를 입력해주세요 : ")
        try:
            a = int(a)
            
            # 깜빡임 동작 중지 (모든 모드 전환 시)
            if blink_active and a != 3:
                blink_active = False
                if blink_thread:
                    blink_thread.join(0.5)  # 스레드 종료 대기 (최대 0.5초)
            
            if a == 0:
                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
            elif a == 1:
                pwm1.ChangeDutyCycle(100)
                pwm2.ChangeDutyCycle(30)
            elif a == 2:
                pwm1.ChangeDutyCycle(30)
                pwm2.ChangeDutyCycle(30)
            elif a == 3:
                # 깜빡임 모드 활성화
                blink_active = True
                blink_thread = threading.Thread(target=blink_leds)
                blink_thread.daemon = True  # 메인 프로그램 종료 시 스레드도 종료
                blink_thread.start()
            elif a == 4:
                pwm1.ChangeDutyCycle(100)
                pwm2.ChangeDutyCycle(100)
            else:
                print("0~4 사이의 값을 입력해주세요.")
                
        except ValueError:
            print("숫자를 입력해주세요.")

except KeyboardInterrupt:
    print("program killed")
    blink_active = False  # 스레드 종료 신호
    if blink_thread:
        blink_thread.join(1.0)  # 스레드 종료 대기
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()  # GPIO 정리
    sys.exit(0)