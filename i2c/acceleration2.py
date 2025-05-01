import smbus #I2C 통신 패키지
import time

# I2C 버스 초기화 (1번 버스 사용)
bus = smbus.SMBus(1)

# MMA845X I2C 주소 (기본값: 0x1C)
MMA845X_ADDRESS = 0x1C
CTRL_REG1 = 0x2A
XYZ_DATA_CFG = 0x0E
msb_address = 0x01
PULSE_CFG = 0x21
PULSE_THSX = 0x23
PULSE_LTCY = 0x27
PULSE_WIND = 0x28

def init_accel():
    bus.write_byte_data(MMA845X_ADDRESS, CTRL_REG1, 0x01) # 400Hz ODR, 활성 모드
    bus.write_byte_data(MMA845X_ADDRESS, PULSE_CFG, 0x7F) # 탭 감지 설정 (X,Y,Z 축 활성화)
    bus.write_byte_data(MMA845X_ADDRESS, PULSE_THSX, 0x08) # 임계값 설정 (0.5g)
    
    # 더블탭 타이밍 설정
    bus.write_byte_data(MMA845X_ADDRESS, PULSE_LTCY, 0x20) # 첫 번째와 두번째 탭 간 최소 대기 시간  0x20 ==> 32 x 1.25ms(Hz 달라짐에 따라 ms 다름)
    bus.write_byte_data(MMA845X_ADDRESS, PULSE_WIND, 0x30) # 두 번째 탭 허용 시간(첫번째 탭 후 대기시간이 지난뒤 더블탭 인지 시간) 0x30 ==> 48 x 1.25ms

# 센서 초기화 함수
def initialize_sensor():
    # Standby 모드 설정
    # bus.write_byte_data(MMA845X_ADDRESS, CTRL_REG1, 0x00)
    init_accel();
    # ±2g 범위 설정
    bus.write_byte_data(MMA845X_ADDRESS, XYZ_DATA_CFG, 0x00)
    # Active 모드 설정
    bus.write_byte_data(MMA845X_ADDRESS, CTRL_REG1, 0x01)
    time.sleep(0.1)

# 읽어오는 코드 작성
def read_acceleration():
    msb_x = bus.read_byte_data(MMA845X_ADDRESS, msb_address)
    lsb_x = bus.read_byte_data(MMA845X_ADDRESS, msb_address +1)
    msb_y = bus.read_byte_data(MMA845X_ADDRESS, msb_address +2)
    lsb_y = bus.read_byte_data(MMA845X_ADDRESS, msb_address +3)
    msb_z = bus.read_byte_data(MMA845X_ADDRESS, msb_address +4)
    lsb_z = bus.read_byte_data(MMA845X_ADDRESS, msb_address +5)
    
    x_value = ((msb_x << 8) | lsb_x) >> 4
    y_value = ((msb_y << 8) | lsb_y) >> 4
    z_value = ((msb_z << 8) | lsb_z) >> 4
    
    if x_value > 2047:
        x_value -= 4096
    if y_value > 2047:
        y_value -= 4096
    if z_value > 2047:
        z_value -= 4096
    
    return x_value/ 1024.0, y_value/1024.0, z_value/1024.0

def result_print(x, y, z):
    # if (y < -0.9 and y > -1.0) and (x > -0.2 and x < 0) and (z > -0.2 and z < 0):
    #     print("기준")
    if x < -0.2:
        print("오")
    elif x > 0.2:
        print("왼")
    elif z < -0.2:
        print("앞")
    elif z > 0.2:
        print("뒤")
    else:
        print("기준")
                
        
# 메인 실행 코드
if __name__ == "__main__":
    try:
        initialize_sensor()        
        while True:
            x, y, z = read_acceleration()
            # result_print(x, y, z)
            print(f"X: {x:.3f}g, Y: {y:.3f}g, Z: {z:.3f}g")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n프로그램 종료")
