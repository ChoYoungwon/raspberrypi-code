import serial
import time

# 시리얼 포트 설정
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

try:
    print("루프백 테스트 시작. TX와 RX가 연결되어 있는지 확인하세요.")
    
    while True:
        test_message = "UART 테스트 " + time.strftime("%H:%M:%S")
        print(f"전송: {test_message}")
        
        # 메시지 전송
        ser.write((test_message + '\r\n').encode('utf-8'))
        
        # 잠시 대기
        time.sleep(0.1)
        
        # 수신 데이터 확인
        if ser.in_waiting > 0:
            received = ser.readline().decode('utf-8').strip()
            print(f"수신: {received}")
            
            # 송신한 메시지와 수신한 메시지 비교
            if received == test_message:
                print("테스트 성공: 메시지가 정확히 수신되었습니다.")
            else:
                print("테스트 실패: 메시지가 다릅니다.")
        else:
            print("수신 데이터 없음. 연결을 확인하세요.")
            
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n테스트 종료")
    ser.close()