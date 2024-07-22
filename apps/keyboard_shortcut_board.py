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

# pyautogui.hotkey('ctrl', 'shift', 'num7')
def button1(event):
    if not board.switch_1:
        pyautogui.press("num1")
    else:
        pyautogui.press("num5")

def button2(event):
    if not board.switch_1:
        pyautogui.press("num2")
    else:
        pyautogui.press("num6")

def button3(event):
    if not board.switch_1:
        pyautogui.press("num3")
    else:
        pyautogui.press("num7")

def button4(event):
    if not board.switch_1:
        pyautogui.press("num4")
    else:
        pyautogui.press("num8")

def button1_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey("ctrl", "num1")
    else:
        pyautogui.hotkey("ctrl", "num5")

def button2_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey("ctrl", "num2")
    else:
        pyautogui.hotkey("ctrl", "num6")

def button3_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey("ctrl", "num3")
    else:
        pyautogui.hotkey("ctrl", "num7")

def button4_ctrl(event):
    if not board.switch_1:
        pyautogui.hotkey("ctrl", "num4")
    else:
        pyautogui.hotkey("ctrl", "num8")

def pot(event, val):
    pyautogui.press("num0")

def initialize_handlers(board):
    board.set_button_handler(Board.BUTTON_1_PRIMARY, button1)
    board.set_button_handler(Board.BUTTON_2_PRIMARY, button2)
    board.set_button_handler(Board.BUTTON_3_PRIMARY, button3)
    board.set_button_handler(Board.BUTTON_4_PRIMARY, button4)
    board.set_button_handler(Board.BUTTON_1_SECONDARY, button1_ctrl)
    board.set_button_handler(Board.BUTTON_2_SECONDARY, button2_ctrl)
    board.set_button_handler(Board.BUTTON_3_SECONDARY, button3_ctrl)
    board.set_button_handler(Board.BUTTON_4_SECONDARY, button4_ctrl)
    board.set_pot_handler(Board.POT_1_VAL, pot)

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
