import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(script_dir, '../communicator')
nircmd_exe = "c://Projects//input-panel//nircmd//nircmd.exe"

sys.path.append(module_dir)
sys.path.append(nircmd_exe)

from ibcp_com import IbcpCom
from board import Board
import signal
import time
import threading

import win32api
import win32con

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from ctypes import cast, POINTER

PROCESS_SPOTIFY = "Spotify.exe"
PROCESS_DISCORD = "Discord.exe"

OUT_DEVICE_MONITOR = "Monitors"
OUT_DEVICE_HEADPHONES = "Austinas"

def press_key(hexKeyCode):
    win32api.keybd_event(hexKeyCode, 0, 0, 0)
    win32api.keybd_event(hexKeyCode, 0, win32con.KEYEVENTF_KEYUP, 0)

def play_pause(event):
    press_key(win32con.VK_MEDIA_PLAY_PAUSE)
    print("Toggled play/pause")

def next_song(event):
    press_key(win32con.VK_MEDIA_NEXT_TRACK)
    print("Skipped to next song")

def previous_song(event):
    press_key(win32con.VK_MEDIA_PREV_TRACK)
    print("Skipped to previous song")

def change_system_volume(event, value):
    volume.SetMasterVolumeLevelScalar(value / 100, None)
    print(f"Set system volume to: {value}%")

def toggle_mute(event):
    if check_current_volume() == 0.0:
        change_system_volume(event, board.pot_1)
        print("System unmuted")
    else:
        change_system_volume(event, 0)
        print("System muted")

def check_current_volume():
    CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = volume.GetMasterVolumeLevelScalar()
        return current_volume
    finally:
        CoUninitialize()

def change_process_volume(process, value):
    CoInitialize()
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == process:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume.SetMasterVolume(value / 100, None)
                print(f"Set {process} volume to: {value}%")
                break
    finally:
        CoUninitialize()

def change_spotify_volume(event, value):
    change_process_volume(PROCESS_SPOTIFY, value)

def change_discord_volume(event, value):
    change_process_volume(PROCESS_DISCORD, value)

def toggle_spotify_volume(event, value):
    board.set_pot_handler(Board.POT_2_VAL, change_spotify_volume)

def toggle_discord_volume(event, value):
    board.set_pot_handler(Board.POT_2_VAL, change_discord_volume)

def set_output(device):
    os.system(f'{nircmd_exe} setdefaultsounddevice "{device}"')

def set_headphones_as_output(event, value):
    print(f"Set headphones as output")
    set_output(OUT_DEVICE_HEADPHONES)

def set_speakers_as_output(event, value):
    print(f"Set speakers as output")
    set_output(OUT_DEVICE_MONITOR)

def initialize_handlers(board):
    board.set_button_handler(Board.BUTTON_1_PRIMARY, previous_song)
    board.set_button_handler(Board.BUTTON_2_PRIMARY, play_pause)
    board.set_button_handler(Board.BUTTON_3_PRIMARY, next_song)
    board.set_button_handler(Board.BUTTON_4_PRIMARY, toggle_mute)

    board.set_switch_handler(Board.SWITCH_1_ON, toggle_discord_volume)
    board.set_switch_handler(Board.SWITCH_1_OFF, toggle_spotify_volume)

    board.set_channel_handler(Board.CHANNEL_1_ON, set_headphones_as_output)
    board.set_channel_handler(Board.CHANNEL_1_OFF, set_speakers_as_output)

    board.set_pot_handler(Board.POT_1_VAL, change_system_volume)
    board.set_pot_handler(Board.POT_2_VAL, change_spotify_volume)

def background_update_task(comms, board):
    while True:
        time.sleep(0.025)
        message = comms.listen()
        if message is None or not message:
            continue

        board.parse_message(message)

if __name__ == "__main__":
    board = None
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    with IbcpCom() as comms:


        initial_status = comms.send_command_and_await_response("STATUS")
        print(f"Initial state:\n{initial_status}")

        board = Board(initial_status)
        initialize_handlers(board)
        change_system_volume(None, board.pot_1)
        change_spotify_volume(None, board.pot_2)
        if board.channel_1:
            set_output(OUT_DEVICE_HEADPHONES)
        else:
            set_output(OUT_DEVICE_MONITOR)
        print("READY...")
        
        background_thread = threading.Thread(target=background_update_task, args=(comms, board))
        background_thread.daemon = True
        background_thread.start()

        while True:
            time.sleep(1)
