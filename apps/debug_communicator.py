import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(script_dir, '../communicator')
sys.path.append(module_dir)

from ibcp_com import IbcpCom
from board import Board

import time
import threading

def initialize_handlers(board):
    board.set_button_handler(Board.BUTTON_1_PRIMARY, on_button_1_primary_press)
    board.set_button_handler(Board.BUTTON_2_PRIMARY, on_button_2_primary_press)
    board.set_button_handler(Board.BUTTON_3_PRIMARY, on_button_3_primary_press)
    board.set_button_handler(Board.BUTTON_4_PRIMARY, on_button_4_primary_press)

    board.set_button_handler(Board.BUTTON_1_SECONDARY, on_button_1_secondary_press)
    board.set_button_handler(Board.BUTTON_2_SECONDARY, on_button_2_secondary_press)
    board.set_button_handler(Board.BUTTON_3_SECONDARY, on_button_3_secondary_press)
    board.set_button_handler(Board.BUTTON_4_SECONDARY, on_button_4_secondary_press)

    board.set_switch_handler(Board.SWITCH_1_ON, on_switch_1_on_change)
    board.set_switch_handler(Board.SWITCH_2_ON, on_switch_2_on_change)
    board.set_switch_handler(Board.SWITCH_1_OFF, on_switch_1_off_change)
    board.set_switch_handler(Board.SWITCH_2_OFF, on_switch_2_off_change)
    
    board.set_channel_handler(Board.CHANNEL_1_ON, on_channel_1_on_change)
    board.set_channel_handler(Board.CHANNEL_2_ON, on_channel_2_on_change)
    board.set_channel_handler(Board.CHANNEL_3_ON, on_channel_3_on_change)
    board.set_channel_handler(Board.CHANNEL_4_ON, on_channel_4_on_change)
    board.set_channel_handler(Board.CHANNEL_1_OFF, on_channel_1_off_change)
    board.set_channel_handler(Board.CHANNEL_2_OFF, on_channel_2_off_change)
    board.set_channel_handler(Board.CHANNEL_3_OFF, on_channel_3_off_change)
    board.set_channel_handler(Board.CHANNEL_4_OFF, on_channel_4_off_change)

    board.set_pot_handler(Board.POT_1_VAL, on_pot_1_change)
    board.set_pot_handler(Board.POT_2_VAL, on_pot_2_change)


def on_button_1_primary_press(event):
    print("Button 1 primary pressed!")
    
def on_button_2_primary_press(event):
    print("Button 2 primary pressed!")

def on_button_3_primary_press(event):
    print("Button 3 primary pressed!")

def on_button_4_primary_press(event):
    print("Button 4 primary pressed!")

def on_button_1_secondary_press(event):
    print("Button 1 secondary pressed!")
    
def on_button_2_secondary_press(event):
    print("Button 2 secondary pressed!")

def on_button_3_secondary_press(event):
    print("Button 3 secondary pressed!")

def on_button_4_secondary_press(event):
    print("Button 4 secondary pressed!")

def on_switch_1_on_change(event, change):
    print(f"Switch 1 turned on, value: {change}")

def on_switch_2_on_change(event, change):
    print(f"Switch 2 turned on, value: {change}")

def on_switch_1_off_change(event, change):
    print(f"Switch 1 turned off, value: {change}")

def on_switch_2_off_change(event, change):
    print(f"Switch 2 turned off, value: {change}")

def on_channel_1_on_change(event, change):
    print(f"Channel 1 turned on, value: {change}")

def on_channel_2_on_change(event, change):
    print(f"Channel 2 turned on, value: {change}")

def on_channel_3_on_change(event, change):
    print(f"Channel 3 turned on, value: {change}")

def on_channel_4_on_change(event, change):
    print(f"Channel 4 turned on, value: {change}")

def on_channel_1_off_change(event, change):
    print(f"Channel 1 turned off, value: {change}")

def on_channel_2_off_change(event, change):
    print(f"Channel 2 turned off, value: {change}")

def on_channel_3_off_change(event, change):
    print(f"Channel 3 turned off, value: {change}")

def on_channel_4_off_change(event, change):
    print(f"Channel 4 turned off, value: {change}")

def on_pot_1_change(event, val):
    print(f"Pot 1 changed to {val}!")

def on_pot_2_change(event, val):
    print(f"Pot 2 changed to {val}!")

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
            print("Main thread is running...")
            print(board.pot_1)
            time.sleep(1)
