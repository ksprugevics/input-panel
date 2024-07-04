import serial
import time

arduino_port = 'COM3'
baud_rate = 9600

try:
    arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=5)
    print(f"Connected to {arduino_port} at {baud_rate} baud")
except serial.SerialException as e:
    print(f"Failed to connect to {arduino_port}: {e}")
    exit()

while True:
    if not arduino.isOpen():
        print("Arduino port is not open.")
        continue
    
    try:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)

    except Exception as e:
        print(f"Error reading from Arduino: {e}")

    time.sleep(0.025)
