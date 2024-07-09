import unittest
import serial
from unittest.mock import MagicMock
from ibcp_com import IbcpCom

class TestIbcpCom(unittest.TestCase):

    def setUp(self):
        self.ibcp = IbcpCom(serial_port="COM3", baud_rate=9600, timeout=5)
        self.ibcp._serial_connection = MagicMock()

    def tearDown(self):
        self.ibcp.close()

    def test_listen(self):
        self.ibcp._serial_connection.isOpen.return_value = True
        self.ibcp._serial_connection.readline.return_value = bytes("SW1-0;SW2-1;CH-SW1-1;CH-SW2-1;CH-SW3-1;CH-SW4-1;POT1-45;POT2-53", "utf-8")

        message = self.ibcp.listen()
        self.assertEqual(message, "SW1-0;SW2-1;CH-SW1-1;CH-SW2-1;CH-SW3-1;CH-SW4-1;POT1-45;POT2-53")

        self.ibcp._serial_connection.isOpen.return_value = False
        message = self.ibcp.listen()
        self.assertIsNone(message)

    def test_send_command_and_await_response(self):
        self.ibcp._serial_connection.isOpen.return_value = True
        self.ibcp._serial_connection.readline.return_value = bytes("SW1-0", "utf-8")
        response = self.ibcp.send_command_and_await_response("STATUS-SW1")
        self.assertEqual(response, "SW1-0")

        self.ibcp._serial_connection.isOpen.return_value = False
        response = self.ibcp.send_command_and_await_response("STATUS-SW1")
        self.assertIsNone(response)
