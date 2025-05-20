import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)
TX_PIN = 14  # GPIO 14 (물리적 핀 8)
RX_PIN = 15  # GPIO 15 (물리적 핀 10)

# 핀 설정
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    print("GPIO 루프백 테스트 시작")
    print("물리적으로 GPIO 14(TX)와 GPIO 15(RX)가 연결되어 있어야 합니다.")
    print("테스트 중 Ctrl+C를 눌러 종료할 수 있습니다.")
    
    while True:
        # TX 핀을 HIGH로 설정
        GPIO.output(TX_PIN, GPIO.HIGH)
        time.sleep(0.5)
        
        # RX 핀 상태 읽기
        rx_state = GPIO.input(RX_PIN)
        print(f"TX: HIGH, RX: {rx_state} - {'성공 ✓' if rx_state else '실패 ✗'}")
        
        # TX 핀을 LOW로 설정
        GPIO.output(TX_PIN, GPIO.LOW)
        time.sleep(0.5)
        
        # RX 핀 상태 읽기
        rx_state = GPIO.input(RX_PIN)
        print(f"TX: LOW, RX: {rx_state} - {'성공 ✓' if not rx_state else '실패 ✗'}")
        
        print("-" * 30)
        
except KeyboardInterrupt:
    print("\n테스트 종료")
finally:
    GPIO.cleanup()