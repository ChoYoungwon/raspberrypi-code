import serial
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

def send_message(msg):
    ser.write(msg.encode('utf-8'))
    print(f"send: {msg}")

def receive_message():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"recieve: {data}")
        return data
    return None

try:
    while True:
        # receive_message()
        # time.sleep(1)
        send_message("test")
        time.sleep(1)

except KeyboardInterrupt:
    print("end\n")
    ser.close()
