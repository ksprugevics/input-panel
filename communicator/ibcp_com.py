import serial
import time

class IbcpCom:
    """Communicator for IBCP version 0.2"""

    def __init__(self, serial_port="COM3", baud_rate=9600, timeout=5, startup_delay=3):
        self._serial_port = serial_port
        self._baud_rate = baud_rate
        self._timeout = timeout
        self._serial_connection = None
        self.create_serial_connection()
        print("Waiting a bit for connection to establish...")
        time.sleep(3)

    def create_serial_connection(self):
        """Create the serial connection."""
        try:
            self._serial_connection = serial.Serial(port=self._serial_port, baudrate=self._baud_rate, timeout=self._timeout)
            print(f"Connection established on {self._serial_port} at {self._baud_rate} baud")
        except serial.SerialException as e:
            print(f"Failed to establish connection on {self._serial_port}. Is it plugged in?\n{e}")
    
    def close(self):
        """Close the serial connection if it's open."""
        if self._serial_connection and self._serial_connection.is_open:
            try:
                self._serial_connection.close()
                print("Serial connection closed")
            except serial.SerialException as e:
                print(f"Failed to close the connection: {e}")

    def listen(self):
        """Listen for a message from the serial connection."""
        try:
            if self._serial_connection and self._serial_connection.isOpen():
                return self._serial_connection.readline().decode("utf-8").rstrip()
            else:
                print("Broken connection")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return None

    def send_command(self, cmd):
        """Send a command via the serial connection."""
        try:
            if self._serial_connection and self._serial_connection.isOpen():
                self._serial_connection.write(bytes(cmd, "utf-8"))
                self._serial_connection.flush()
                print("Command sent: " + cmd)
            else:
                print("Broken connection")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")

    def send_command_and_await_response(self, cmd):
        """Send a command and wait for a response."""
        self.send_command(cmd)
        return self.listen()

    @property
    def serial_connection(self):
        """Get the serial connection."""
        return self._serial_connection
    
    @serial_connection.setter
    def serial_connection(self, serial_connection):
        """Set the serial connection."""
        self._serial_connection = serial_connection

    def __del__(self):
        """Ensure the serial connection is closed upon object deletion."""
        self.close()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.close()
