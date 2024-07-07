from receiver import Receiver
from board import Board
import signal
import time

def graceful_exit(signal, frame, rec):
    print("Stopping receiver and closing serial connection...")
    del rec
    exit(0)

def onButton1PrimaryPress():
    print("Button 1 primary pressed!")
    
def onButton2PrimaryPress():
    print("Button 2 primary pressed!")

def onButton3PrimaryPress():
    print("Button 3 primary pressed!")

def onButton4PrimaryPress():
    print("Button 4 primary pressed!")

def onButton1SecondaryPress():
    print("Button 1 secondary pressed!")
    
def onButton2SecondaryPress():
    print("Button 2 secondary pressed!")

def onButton3SecondaryPress():
    print("Button 3 secondary pressed!")

def onButton4SecondaryPress():
    print("Button 4 secondary pressed!")

def onSwitch1OnChange(change):
    print(f"Switch 1 turned on, value: {change}")

def onSwitch2OnChange(change):
    print(f"Switch 2 turned on, value: {change}")

def onSwitch1OffChange(change):
    print(f"Switch 1 turned off, value: {change}")

def onSwitch2OffChange(change):
    print(f"Switch 2 turned off, value: {change}")

def onChannel1OnChange(change):
    print(f"Channel 1 turned on, value: {change}")

def onChannel2OnChange(change):
    print(f"Channel 2 turned on, value: {change}")

def onChannel3OnChange(change):
    print(f"Channel 3 turned on, value: {change}")

def onChannel4OnChange(change):
    print(f"Channel 4 turned on, value: {change}")

def onChannel1OffChange(change):
    print(f"Channel 1 turned off, value: {change}")

def onChannel2OffChange(change):
    print(f"Channel 2 turned off, value: {change}")

def onChannel3OffChange(change):
    print(f"Channel 3 turned off, value: {change}")

def onChannel4OffChange(change):
    print(f"Channel 4 turned off, value: {change}")

def onPot1Change(val):
    print(f"Pot 1 changed to {val}!")

def onPot2Change(val):
    print(f"Pot 2 changed to {val}!")

if __name__ == "__main__":
    rec = Receiver()
    board = Board()

    board.setButtonHandler(Board._BUTTON_1_PRIMARY, onButton1PrimaryPress)
    board.setButtonHandler(Board._BUTTON_2_PRIMARY, onButton2PrimaryPress)
    board.setButtonHandler(Board._BUTTON_3_PRIMARY, onButton3PrimaryPress)
    board.setButtonHandler(Board._BUTTON_4_PRIMARY, onButton4PrimaryPress)

    board.setButtonHandler(Board._BUTTON_1_SECONDARY, onButton1SecondaryPress)
    board.setButtonHandler(Board._BUTTON_2_SECONDARY, onButton2SecondaryPress)
    board.setButtonHandler(Board._BUTTON_3_SECONDARY, onButton3SecondaryPress)
    board.setButtonHandler(Board._BUTTON_4_SECONDARY, onButton4SecondaryPress)

    board.setSwitchHandler(Board._SWITCH_1_ON, onSwitch1OnChange)
    board.setSwitchHandler(Board._SWITCH_2_ON, onSwitch2OnChange)
    board.setSwitchHandler(Board._SWITCH_1_OFF, onSwitch1OffChange)
    board.setSwitchHandler(Board._SWITCH_2_OFF, onSwitch2OffChange)
    
    board.setChannelHandler(Board._CHANNEL_1_ON, onChannel1OnChange)
    board.setChannelHandler(Board._CHANNEL_2_ON, onChannel2OnChange)
    board.setChannelHandler(Board._CHANNEL_3_ON, onChannel3OnChange)
    board.setChannelHandler(Board._CHANNEL_4_ON, onChannel4OnChange)
    board.setChannelHandler(Board._CHANNEL_1_OFF, onChannel1OffChange)
    board.setChannelHandler(Board._CHANNEL_2_OFF, onChannel2OffChange)
    board.setChannelHandler(Board._CHANNEL_3_OFF, onChannel3OffChange)
    board.setChannelHandler(Board._CHANNEL_4_OFF, onChannel4OffChange)

    board.setPotHandler(Board._POT_1_VAL, onPot1Change)
    board.setPotHandler(Board._POT_2_VAL, onPot2Change)

    signal.signal(signal.SIGINT, lambda sig, frame: graceful_exit(sig, frame, rec))

    while True:
        time.sleep(0.025)
        message = rec.listen()
        if message is None or not message:
            continue

        board.parseMessage(message)
        # print(board)
