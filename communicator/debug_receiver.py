from ibcp_com import IbcpCom
from board import Board
import signal
import time

def initializeHandlers(board):
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


def onButton1PrimaryPress(event):
    print("Button 1 primary pressed!")
    
def onButton2PrimaryPress(event):
    print("Button 2 primary pressed!")

def onButton3PrimaryPress(event):
    print("Button 3 primary pressed!")

def onButton4PrimaryPress(event):
    print("Button 4 primary pressed!")

def onButton1SecondaryPress(event):
    print("Button 1 secondary pressed!")
    
def onButton2SecondaryPress(event):
    print("Button 2 secondary pressed!")

def onButton3SecondaryPress(event):
    print("Button 3 secondary pressed!")

def onButton4SecondaryPress(event):
    print("Button 4 secondary pressed!")

def onSwitch1OnChange(event, change):
    print(f"Switch 1 turned on, value: {change}")

def onSwitch2OnChange(event, change):
    print(f"Switch 2 turned on, value: {change}")

def onSwitch1OffChange(event, change):
    print(f"Switch 1 turned off, value: {change}")

def onSwitch2OffChange(event, change):
    print(f"Switch 2 turned off, value: {change}")

def onChannel1OnChange(event, change):
    print(f"Channel 1 turned on, value: {change}")

def onChannel2OnChange(event, change):
    print(f"Channel 2 turned on, value: {change}")

def onChannel3OnChange(event, change):
    print(f"Channel 3 turned on, value: {change}")

def onChannel4OnChange(event, change):
    print(f"Channel 4 turned on, value: {change}")

def onChannel1OffChange(event, change):
    print(f"Channel 1 turned off, value: {change}")

def onChannel2OffChange(event, change):
    print(f"Channel 2 turned off, value: {change}")

def onChannel3OffChange(event, change):
    print(f"Channel 3 turned off, value: {change}")

def onChannel4OffChange(event, change):
    print(f"Channel 4 turned off, value: {change}")

def onPot1Change(event, val):
    print(f"Pot 1 changed to {val}!")

def onPot2Change(event, val):
    print(f"Pot 2 changed to {val}!")

def graceful_exit(signal, frame, comms):
    print("Stopping Communicator and closing serial connection...")
    del comms
    exit(0)

if __name__ == "__main__":
    with IbcpCom() as comms:
        print("Waiting a bit for connection to establish...")
        time.sleep(3)
        signal.signal(signal.SIGINT, lambda sig, frame: graceful_exit(sig, frame, comms))

        initialStatus = comms.send_command_and_await_response("STATUS")
        print(f"Initial state:\n{initialStatus}")

        board = Board(initialStatus)
        initializeHandlers(board)
        
        while True:
            time.sleep(0.025)
            message = comms.listen()
            if message is None or not message:
                continue

            board.parseMessage(message)
            # print(board)
