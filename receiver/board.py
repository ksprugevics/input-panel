# Responsible for keeping track of state and parsing messages
class Board:

    _BUTTON_1_PRIMARY = "B1A"
    _BUTTON_2_PRIMARY = "B2A"
    _BUTTON_3_PRIMARY = "B3A"
    _BUTTON_4_PRIMARY = "B4A"
    _BUTTON_1_SECONDARY = "B1B"
    _BUTTON_2_SECONDARY = "B2B"
    _BUTTON_3_SECONDARY = "B3B"
    _BUTTON_4_SECONDARY = "B4B"

    _SWITCH_1_ON = "SW1-1"
    _SWITCH_2_ON = "SW2-1"
    _SWITCH_1_OFF = "SW1-0"
    _SWITCH_2_OFF = "SW2-0"

    _CHANNEL_1_ON = "CH-SW1-1"
    _CHANNEL_2_ON = "CH-SW2-1"
    _CHANNEL_3_ON = "CH-SW3-1"
    _CHANNEL_4_ON = "CH-SW4-1"
    _CHANNEL_1_OFF = "CH-SW1-0"
    _CHANNEL_2_OFF = "CH-SW2-0"
    _CHANNEL_3_OFF = "CH-SW3-0"
    _CHANNEL_4_OFF = "CH-SW4-0"

    _POT_1_VAL = "POT1-"
    _POT_2_VAL = "POT2-"

    def __init__(self, initialStatus=None):
        self.switch_1 = False
        self.switch_2 = False

        self.channel_1 = False
        self.channel_2 = False
        self.channel_3 = False
        self.channel_4 = False

        self.pot_1 = 0
        self.pot_2 = 0

        self._button_handlers = {
            self._BUTTON_1_PRIMARY: self.eventNotMapped,
            self._BUTTON_2_PRIMARY: self.eventNotMapped,
            self._BUTTON_3_PRIMARY: self.eventNotMapped,
            self._BUTTON_4_PRIMARY: self.eventNotMapped,
            self._BUTTON_1_SECONDARY: self.eventNotMapped,
            self._BUTTON_2_SECONDARY: self.eventNotMapped,
            self._BUTTON_3_SECONDARY: self.eventNotMapped,
            self._BUTTON_4_SECONDARY: self.eventNotMapped
        }

        self._switch_handlers = {
            self._SWITCH_1_ON: self.eventNotMapped,
            self._SWITCH_2_ON: self.eventNotMapped,
            self._SWITCH_1_OFF: self.eventNotMapped,
            self._SWITCH_2_OFF: self.eventNotMapped
        }

        self._channel_handlers = {
            self._CHANNEL_1_ON: self.eventNotMapped,
            self._CHANNEL_2_ON: self.eventNotMapped,
            self._CHANNEL_3_ON: self.eventNotMapped,
            self._CHANNEL_4_ON: self.eventNotMapped,
            self._CHANNEL_1_OFF: self.eventNotMapped,
            self._CHANNEL_2_OFF: self.eventNotMapped,
            self._CHANNEL_3_OFF: self.eventNotMapped,
            self._CHANNEL_4_OFF: self.eventNotMapped
        }

        self._pot_handlers = {
            self._POT_1_VAL: self.eventNotMapped,
            self._POT_2_VAL: self.eventNotMapped
        }

        if initialStatus is not None:
            states = initialStatus.split(";")
            self.checkSwitchEvent(states[0])
            self.checkSwitchEvent(states[1])
            self.checkChannelSwitchEvent(states[2])
            self.checkChannelSwitchEvent(states[3])
            self.checkChannelSwitchEvent(states[4])
            self.checkChannelSwitchEvent(states[5])
            self.checkPotChangeEvent(states[6])
            self.checkPotChangeEvent(states[7])
            print("Initialized board from given status")
            print(self)

    def eventNotMapped(self, event, *args):
        print(f"Event {event} is not mapped")

    def __str__(self):
        return (f"Board(\n"
                f"    switch_1 = {self.switch_1},\n"
                f"    switch_2 = {self.switch_2},\n"
                f"    channel_1 = {self.channel_1},\n"
                f"    channel_2 = {self.channel_2},\n"
                f"    channel_3 = {self.channel_3},\n"
                f"    channel_4 = {self.channel_4},\n"
                f"    pot_1    = {self.pot_1},\n"
                f"    pot_2    = {self.pot_2}\n"
                f")")

    def parseMessage(self, msg):
        self.checkButtonEvent(msg)
        self.checkSwitchEvent(msg)
        self.checkChannelSwitchEvent(msg)
        self.checkPotChangeEvent(msg)

    def checkButtonEvent(self, msg):
        if msg in self._button_handlers and self._button_handlers[msg] is not None:
            self._button_handlers[msg](msg)

    def checkSwitchEvent(self, msg):
        if msg == self._SWITCH_1_ON:
            self.switch_1 = True
            self._switch_handlers[msg](self._SWITCH_1_ON, True)
        elif msg == self._SWITCH_1_OFF:
            self.switch_1 = False
            self._switch_handlers[msg](self._SWITCH_1_OFF, False)

        if msg == self._SWITCH_2_ON:
            self.switch_2 = True
            self._switch_handlers[msg](self._SWITCH_2_ON, True)
        elif msg == self._SWITCH_2_OFF:
            self.switch_2 = False
            self._switch_handlers[msg](self._SWITCH_2_OFF, False)

    def checkChannelSwitchEvent(self, msg):
        if msg == self._CHANNEL_1_ON:
            self.channel_1 = True
            self._channel_handlers[msg](self._CHANNEL_1_ON, True)
        elif msg == self._CHANNEL_1_OFF:
            self.channel_1 = False
            self._channel_handlers[msg](self._CHANNEL_1_OFF, False)

        if msg == self._CHANNEL_2_ON:
            self.channel_2 = True
            self._channel_handlers[msg](self._CHANNEL_2_ON, True)
        elif msg == self._CHANNEL_2_OFF:
            self.channel_2 = False
            self._channel_handlers[msg](self._CHANNEL_2_OFF, False)

        if msg == self._CHANNEL_3_ON:
            self.channel_3 = True
            self._channel_handlers[msg](self._CHANNEL_3_ON, True)
        elif msg == self._CHANNEL_3_OFF:
            self.channel_3 = False
            self._channel_handlers[msg](self._CHANNEL_3_OFF, False)

        if msg == self._CHANNEL_4_ON:
            self.channel_4 = True
            self._channel_handlers[msg](self._CHANNEL_4_ON, True)
        elif msg == self._CHANNEL_4_OFF:
            self._channel_handlers[msg](self._CHANNEL_4_OFF, False)

    def checkPotChangeEvent(self, msg):
        if self._POT_1_VAL in msg:
            value = int(msg.split("-")[1])
            if value != self.pot_1:
                self.pot_1 = value
                self._pot_handlers[self._POT_1_VAL](self._POT_1_VAL, value)

        if self._POT_2_VAL in msg:
            value = int(msg.split("-")[1])
            if value != self.pot_2:
                self.pot_2 = value
                self._pot_handlers[self._POT_2_VAL](self._POT_2_VAL, value)

    # Event handler setters
    def setButtonHandler(self, button, handler):
        if button in self._button_handlers:
            self._button_handlers[button] = handler

    def setButtonHandler(self, button, handler):
        if button in self._button_handlers:
            self._button_handlers[button] = handler

    def setSwitchHandler(self, switch, handler):
        if switch in self._switch_handlers:
            self._switch_handlers[switch] = handler

    def setChannelHandler(self, channel, handler):
        if channel in self._channel_handlers:
            self._channel_handlers[channel] = handler

    def setPotHandler(self, pot, handler):
        if pot in self._pot_handlers:
            self._pot_handlers[pot] = handler

    # Field getters & setters
    @property
    def switch_1(self):
        return self._switch_1

    @switch_1.setter
    def switch_1(self, switch_1):
        self._switch_1 = switch_1

    @property
    def switch_2(self):
        return self._switch_2

    @switch_2.setter
    def switch_2(self, switch_2):
        self._switch_2 = switch_2

    @property
    def channel_1(self):
        return self._channel_1

    @channel_1.setter
    def channel_1(self, channel_1):
        self._channel_1 = channel_1

    @property
    def channel_2(self):
        return self._channel_2

    @channel_2.setter
    def channel_2(self, channel_2):
        self._channel_2 = channel_2

    @property
    def channel_3(self):
        return self._channel_3

    @channel_3.setter
    def channel_3(self, channel_3):
        self._channel_3 = channel_3

    @property
    def channel_4(self):
        return self._channel_4

    @channel_4.setter
    def channel_4(self, channel_4):
        self._channel_4 = channel_4

    @property
    def pot_1(self):
        return self._pot_1

    @pot_1.setter
    def pot_1(self, pot_1):
        self._pot_1 = pot_1

    @property
    def pot_2(self):
        return self._pot_2

    @pot_2.setter
    def pot_2(self, pot_2):
        self._pot_2 = pot_2
