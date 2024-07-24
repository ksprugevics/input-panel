import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(script_dir, '../communicator')
sys.path.append(module_dir)

from ibcp_com import IbcpCom
from board import Board

import time
import threading
import pyautogui

# https://pyautogui.readthedocs.io/en/latest/keyboard.html
B1 = "num1"
B2 = "num2"
B3 = "num3"
B4 = "num4"

# 5-8 activate when SW1 is on
B5 = "num5"
B6 = "num6"
B7 = "num7"
B8 = "num8"

SECONDARY_BUTTON_MULTIPLIER = "ctrl"

P1 = "num0"
P2 = "num0"

# 3-4 activate when SW1 is on
P3 = "num0"
P4 = "num0"

def button1(event):
    if not board.switch_1:
        pyautogui.press(B1)
    else:
        pyautogui.press(B5)

def button2(event):
    if not board.switch_1:
        pyautogui.press(B2)
    else:
        pyautogui.press(B6)

def button3(event):
    if not board.switch_1:
        pyautogui.press(B3)
    else:
        pyautogui.press(B7)

def button4(event):
    if not board.switch_1:
        pyautogui.press(B4)
    else:
        pyautogui.press(B8)

def button1_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B1)
    else:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B5)

def button2_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B2)
    else:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B6)

def button3_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B3)
    else:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B7)

def button4_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B4)
    else:
        pyautogui.hotkey(SECONDARY_BUTTON_MULTIPLIER, B8)

def pot1(event, val):
    if not board.switch_1:
        pyautogui.press(P1)
    else:
        pyautogui.press(P3)

def pot2(event, val):
    if not board.switch_1:
        pyautogui.press(P2)
    else:
        pyautogui.press(P4)

def initialize_handlers(board):
    board.set_button_handler(Board.BUTTON_1_PRIMARY, button1)
    board.set_button_handler(Board.BUTTON_2_PRIMARY, button2)
    board.set_button_handler(Board.BUTTON_3_PRIMARY, button3)
    board.set_button_handler(Board.BUTTON_4_PRIMARY, button4)
    board.set_button_handler(Board.BUTTON_1_SECONDARY, button1_ctrl)
    board.set_button_handler(Board.BUTTON_2_SECONDARY, button2_ctrl)
    board.set_button_handler(Board.BUTTON_3_SECONDARY, button3_ctrl)
    board.set_button_handler(Board.BUTTON_4_SECONDARY, button4_ctrl)
    board.set_pot_handler(Board.POT_1_VAL, pot1)
    board.set_pot_handler(Board.POT_2_VAL, pot2)

def background_update_task(comms, board):
    while True:
        time.sleep(0.025)
        message = comms.listen()
        if message is None or not message:
            continue

        board.parse_message(message)

if __name__ == "__main__":
    with IbcpCom() as comms:

        initial_status = comms.send_command_and_await_response("STATUS")
        print(f"Initial state:\n{initial_status}")

        board = Board(initial_status)
        initialize_handlers(board)
        print("READY...")
        
        background_thread = threading.Thread(target=background_update_task, args=(comms, board))
        background_thread.daemon = True
        background_thread.start()

        while True:
            time.sleep(1)
