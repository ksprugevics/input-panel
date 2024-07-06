# Version 0.1
import serial
import time
import win32api
import win32con

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

def press_key(hexKeyCode):
    win32api.keybd_event(hexKeyCode, 0, 0, 0)
    win32api.keybd_event(hexKeyCode, 0, win32con.KEYEVENTF_KEYUP, 0)

# Play/Pause function
def play_pause():
    press_key(win32con.VK_MEDIA_PLAY_PAUSE)
    print("Toggled play/pause")

# Next song function
def next_song():
    press_key(win32con.VK_MEDIA_NEXT_TRACK)
    print("Skipped to next song")

# Previous song function
def previous_song():
    press_key(win32con.VK_MEDIA_PREV_TRACK)
    print("Skipped to previous song")



def potEventController(pot1, pot2, new_pot1, new_pot2):
    if new_pot1 != pot1 : pot1 = new_pot1
    if new_pot2 != pot2:
        pot2 = new_pot2
        new_volume = pot2 / 100
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        print(f"Set volume to: {pot2}%")

    return pot1, pot2


def buttonEventController(button_press_event):
    if button_press_event[0] == "1" : return 1
    if button_press_event[1] == "1" : return 2
    if button_press_event[2] == "1" : return 3
    if button_press_event[3] == "1" : return 4
    if button_press_event[4] == "1" : return 0

arduino_port = 'COM3'
baud_rate = 9600

channel = 0
switch1 = False
switch2 = False
pot1 = 0
pot2 = 0

debounce_delay = 0.25

# Get default audio device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
last_button_press_time = time.time()

try:
    arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=5)
    print(f"Connected to {arduino_port} at {baud_rate} baud")
except serial.SerialException as e:
    print(f"Failed to connect to {arduino_port}: {e}")
    exit()

while True:
    if not arduino.isOpen():
        print("Arduino port is not open.")
        continue
    
    try:
        if arduino.in_waiting <= 0:
            continue

        in_string = arduino.readline().decode('utf-8').rstrip()
        # print(in_string)
        values = in_string.split("-")
        channel = values[0]

        switch1 = True if values[1][0] == "1" else False
        switch2 = True if values[1][1] == "1" else False

        pot1, pot2 = potEventController(pot1, pot2, int(values[3]), int(values[4]))

        button_press = buttonEventController(values[2])

        current_time = time.time()
        if button_press is None:
            continue
        elif current_time - last_button_press_time > debounce_delay:
            if button_press == 1:
                previous_song()
            elif button_press == 2:
                play_pause()
            elif button_press == 3:
                next_song()
        last_button_press_time = current_time
        
        time.sleep(0.025)


    except Exception as e:
        print(f"Error reading from Arduino: {e}")
