import serial

# Receiver for IBCP version 0.1
class Receiver:

    _ARDUINO_PORT = 'COM3'
    _BAUD_RATE = 9600
    _TIMEOUT = 5

    serial_connection = None
    
    def __init__(self):
        self.createSerialConnection()

    def __del__(self):
        self.close()

    def createSerialConnection(self):
        try:
            self.serial_connection = serial.Serial(port=self._ARDUINO_PORT, baudrate=self._BAUD_RATE, timeout=self._TIMEOUT)
            print(f"Connection established on {self._ARDUINO_PORT} at {self._BAUD_RATE} baud")
        except serial.SerialException as e:
            print(f"Failed to establish connection on {self._ARDUINO_PORT}. Is it plugged in?\n{e}")
            exit()
    
    def close(self):
        if self.serial_connection and self.serial_connection.isOpen():
            self.serial_connection.close()
            print("Serial connection closed")

    def listen(self):
        try:
            if self.serial_connection and self.serial_connection.isOpen():
                return self.serial_connection.readline().decode('utf-8').rstrip()
            else:
                print("Broken connection")
                return None
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return None

    # Getters & setters
    @property
    def serial_connection(self):
        return self._serial_connection
    
    @serial_connection.setter
    def serial_connection(self, serial_connection):
        self._serial_connection = serial_connection
