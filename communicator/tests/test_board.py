import unittest
from board import Board
from parameterized import parameterized

class TestBoard(unittest.TestCase):
    
    def test_initialization(self):
        board = Board()
        self.assertFalse(board.switch_1)
        self.assertFalse(board.switch_2)
        self.assertFalse(board.channel_1)
        self.assertFalse(board.channel_2)
        self.assertFalse(board.channel_3)
        self.assertFalse(board.channel_4)
        self.assertEqual(board.pot_1, 0)
        self.assertEqual(board.pot_2, 0)

    def test_initial_status(self):
        status = "SW1-1;SW2-0;CH-SW1-1;CH-SW2-0;CH-SW3-1;CH-SW4-0;POT1-5;POT2-10"
        board = Board(status)
        self.assertTrue(board.switch_1)
        self.assertFalse(board.switch_2)
        self.assertTrue(board.channel_1)
        self.assertFalse(board.channel_2)
        self.assertTrue(board.channel_3)
        self.assertFalse(board.channel_4)
        self.assertEqual(board.pot_1, 5)
        self.assertEqual(board.pot_2, 10)

    @parameterized.expand([
        ("SW1-1", True, False),
        ("SW2-1", False, True),
        ("SW1-0", False, False),
        ("SW2-0", False, False),
    ])
    def test_parse_switch_event(self, msg, switch_1_expected, switch_2_expected):
        board = Board()
        board.parse_message(msg)
        self.assertEqual(board.switch_1, switch_1_expected)
        self.assertEqual(board.switch_2, switch_2_expected)

    @parameterized.expand([
        ("CH-SW1-1", True, False, False, False),
        ("CH-SW2-1", False, True, False, False),
        ("CH-SW3-1", False, False, True, False),
        ("CH-SW4-1", False, False, False, True),
        ("CH-SW1-0", False, False, False, False),
        ("CH-SW2-0", False, False, False, False),
        ("CH-SW3-0", False, False, False, False),
        ("CH-SW4-0", False, False, False, False),
    ])
    def test_parse_channel_event(self, msg, ch1_expected, ch2_expected, ch3_expected, ch4_expected):
        board = Board()
        board.parse_message(msg)
        self.assertEqual(board.channel_1, ch1_expected)
        self.assertEqual(board.channel_2, ch2_expected)
        self.assertEqual(board.channel_3, ch3_expected)
        self.assertEqual(board.channel_4, ch4_expected)

    @parameterized.expand([
        ("POT1-10", 10, 0),
        ("POT2-20", 0, 20),
        ("POT1-0", 0, 0),
        ("POT2-0", 0, 0),
    ])
    def test_parse_pot_event(self, msg, pot1_expected, pot2_expected):
        board = Board()
        board.parse_message(msg)
        self.assertEqual(board.pot_1, pot1_expected)
        self.assertEqual(board.pot_2, pot2_expected)

    @parameterized.expand([
        (Board.BUTTON_1_PRIMARY, ),
        (Board.BUTTON_2_PRIMARY, ),
        (Board.BUTTON_3_PRIMARY, ),
        (Board.BUTTON_4_PRIMARY, ),
        (Board.BUTTON_1_SECONDARY, ),
        (Board.BUTTON_2_SECONDARY, ),
        (Board.BUTTON_3_SECONDARY, ),
        (Board.BUTTON_4_SECONDARY, ),
    ])
    def test_parse_button_event(self, button):
        board = Board()
        
        def button_handler(event):
            self.assertEqual(event, button)

        board.set_button_handler(button, button_handler)
        board.parse_message(button)

    @parameterized.expand([
        (Board.SWITCH_1_ON, True),
        (Board.SWITCH_1_OFF, False),
        (Board.SWITCH_2_ON, True),
        (Board.SWITCH_2_OFF, False),
    ])
    def test_switch_handler(self, switch, state):
        board = Board()
        state_list = []
        
        def switch_handler(event, state_received):
            self.assertEqual(event, switch)
            self.assertEqual(state_received, state)
            state_list.append(state_received)

        board.set_switch_handler(switch, switch_handler)
        board.parse_message(switch)
        self.assertEqual(state_list[-1], state)

    @parameterized.expand([
        (Board.CHANNEL_1_ON, True),
        (Board.CHANNEL_1_OFF, False),
        (Board.CHANNEL_2_ON, True),
        (Board.CHANNEL_2_OFF, False),
        (Board.CHANNEL_3_ON, True),
        (Board.CHANNEL_3_OFF, False),
        (Board.CHANNEL_4_ON, True),
        (Board.CHANNEL_4_OFF, False),
    ])
    def test_channel_handler(self, channel, state):
        board = Board()
        state_list = []
        
        def channel_handler(event, state_received):
            self.assertEqual(event, channel)
            self.assertEqual(state_received, state)
            state_list.append(state_received)

        board.set_channel_handler(channel, channel_handler)
        board.parse_message(channel)
        self.assertEqual(state_list[-1], state)

    @parameterized.expand([
        ("POT1-42", Board.POT_1_VAL, 42),
        ("POT2-85", Board.POT_2_VAL, 85),
    ])
    def test_pot_handler(self, msg, pot, value):
        board = Board()
        value_list = []
        
        def pot_handler(event, value_received):
            self.assertEqual(event, pot)
            self.assertEqual(value_received, value)
            value_list.append(value_received)

        board.set_pot_handler(pot, pot_handler)
        board.parse_message(msg)
        self.assertEqual(value_list[-1], value)
