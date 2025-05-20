import serial
import time

# 테스트할 baudrate 목록
baudrates = [9600, 115200, 57600, 38400, 19200, 4800]

for baudrate in baudrates:
    try:
        print(f"\n=== Baudrate {baudrate} 테스트 ===")
        
        # 시리얼 포트 열기
        ser = serial.Serial(
            port='/dev/serial0',
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print(f"시리얼 포트 열기 성공: {ser.name}")
        
        # 버퍼 초기화
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # 테스트 메시지 전송
        message = f"테스트 {baudrate} bps"
        print(f"전송: {message}")
        
        ser.write((message + '\r\n').encode('utf-8'))
        ser.flush()
        
        # 잠시 대기
        time.sleep(0.5)
        
        # 수신 확인
        if ser.in_waiting > 0:
            received = ser.readline().decode('utf-8').strip()
            print(f"수신: {received}")
            
            if message in received:
                print("✅ 성공: 메시지가 정확히 수신되었습니다!")
            else:
                print("❌ 실패: 수신된 메시지가 다릅니다.")
        else:
            print("❌ 수신 데이터가 없습니다.")
        
        ser.close()
        
    except Exception as e:
        print(f"오류: {e}")
        
    print("-" * 40)

print("\n모든 baudrate 테스트 완료")