class Board:
    """Data class that represents the state of the input board"""

    BUTTON_1_PRIMARY = "B1A"
    BUTTON_2_PRIMARY = "B2A"
    BUTTON_3_PRIMARY = "B3A"
    BUTTON_4_PRIMARY = "B4A"
    BUTTON_1_SECONDARY = "B1B"
    BUTTON_2_SECONDARY = "B2B"
    BUTTON_3_SECONDARY = "B3B"
    BUTTON_4_SECONDARY = "B4B"

    SWITCH_1_ON = "SW1-1"
    SWITCH_2_ON = "SW2-1"
    SWITCH_1_OFF = "SW1-0"
    SWITCH_2_OFF = "SW2-0"

    CHANNEL_1_ON = "CH-SW1-1"
    CHANNEL_2_ON = "CH-SW2-1"
    CHANNEL_3_ON = "CH-SW3-1"
    CHANNEL_4_ON = "CH-SW4-1"
    CHANNEL_1_OFF = "CH-SW1-0"
    CHANNEL_2_OFF = "CH-SW2-0"
    CHANNEL_3_OFF = "CH-SW3-0"
    CHANNEL_4_OFF = "CH-SW4-0"

    POT_1_VAL = "POT1-"
    POT_2_VAL = "POT2-"

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
            self.BUTTON_1_PRIMARY: self.event_not_mapped,
            self.BUTTON_2_PRIMARY: self.event_not_mapped,
            self.BUTTON_3_PRIMARY: self.event_not_mapped,
            self.BUTTON_4_PRIMARY: self.event_not_mapped,
            self.BUTTON_1_SECONDARY: self.event_not_mapped,
            self.BUTTON_2_SECONDARY: self.event_not_mapped,
            self.BUTTON_3_SECONDARY: self.event_not_mapped,
            self.BUTTON_4_SECONDARY: self.event_not_mapped
        }

        self._switch_handlers = {
            self.SWITCH_1_ON: self.event_not_mapped,
            self.SWITCH_2_ON: self.event_not_mapped,
            self.SWITCH_1_OFF: self.event_not_mapped,
            self.SWITCH_2_OFF: self.event_not_mapped
        }

        self._channel_handlers = {
            self.CHANNEL_1_ON: self.event_not_mapped,
            self.CHANNEL_2_ON: self.event_not_mapped,
            self.CHANNEL_3_ON: self.event_not_mapped,
            self.CHANNEL_4_ON: self.event_not_mapped,
            self.CHANNEL_1_OFF: self.event_not_mapped,
            self.CHANNEL_2_OFF: self.event_not_mapped,
            self.CHANNEL_3_OFF: self.event_not_mapped,
            self.CHANNEL_4_OFF: self.event_not_mapped
        }

        self._pot_handlers = {
            self.POT_1_VAL: self.event_not_mapped,
            self.POT_2_VAL: self.event_not_mapped
        }
        
        if initialStatus is not None:
            self.init_status(initialStatus)

    def init_status(self, status):
            """Initialize the board from STATUS command"""
            states = status.split(";")
            self.check_switch_event(states[0])
            self.check_switch_event(states[1])
            self.check_channel_switch_event(states[2])
            self.check_channel_switch_event(states[3])
            self.check_channel_switch_event(states[4])
            self.check_channel_switch_event(states[5])
            self.check_pot_change_event(states[6])
            self.check_pot_change_event(states[7])
            print("Initialized board from given status")
            print(self)

    def event_not_mapped(self, event, *args):
        """Default method when handler is not defined"""
        print(f"Event {event} is not mapped")
  
    def parse_message(self, msg):
        """Parse a received serial message"""
        self.check_button_event(msg)
        self.check_switch_event(msg)
        self.check_channel_switch_event(msg)
        self.check_pot_change_event(msg)

    def check_button_event(self, msg):
        """If message was a button press, execute button handlers"""
        if msg in self._button_handlers and self._button_handlers[msg] is not None:
            self._button_handlers[msg](msg)

    def check_switch_event(self, msg):
        """If message was a switch, execute switch handlers"""
        if msg == self.SWITCH_1_ON:
            self.switch_1 = True
            self._switch_handlers[msg](self.SWITCH_1_ON, True)
        elif msg == self.SWITCH_1_OFF:
            self.switch_1 = False
            self._switch_handlers[msg](self.SWITCH_1_OFF, False)

        if msg == self.SWITCH_2_ON:
            self.switch_2 = True
            self._switch_handlers[msg](self.SWITCH_2_ON, True)
        elif msg == self.SWITCH_2_OFF:
            self.switch_2 = False
            self._switch_handlers[msg](self.SWITCH_2_OFF, False)

    def check_channel_switch_event(self, msg):
        """If message was a channel switch, execute chanel switch handlers"""
        if msg == self.CHANNEL_1_ON:
            self.channel_1 = True
            self._channel_handlers[msg](self.CHANNEL_1_ON, True)
        elif msg == self.CHANNEL_1_OFF:
            self.channel_1 = False
            self._channel_handlers[msg](self.CHANNEL_1_OFF, False)

        if msg == self.CHANNEL_2_ON:
            self.channel_2 = True
            self._channel_handlers[msg](self.CHANNEL_2_ON, True)
        elif msg == self.CHANNEL_2_OFF:
            self.channel_2 = False
            self._channel_handlers[msg](self.CHANNEL_2_OFF, False)

        if msg == self.CHANNEL_3_ON:
            self.channel_3 = True
            self._channel_handlers[msg](self.CHANNEL_3_ON, True)
        elif msg == self.CHANNEL_3_OFF:
            self.channel_3 = False
            self._channel_handlers[msg](self.CHANNEL_3_OFF, False)

        if msg == self.CHANNEL_4_ON:
            self.channel_4 = True
            self._channel_handlers[msg](self.CHANNEL_4_ON, True)
        elif msg == self.CHANNEL_4_OFF:
            self._channel_handlers[msg](self.CHANNEL_4_OFF, False)

    def check_pot_change_event(self, msg):
        """If message was a pot change, execute pot handlers"""
        if self.POT_1_VAL in msg:
            value = int(msg.split("-")[1])
            if value != self.pot_1:
                self.pot_1 = value
                self._pot_handlers[self.POT_1_VAL](self.POT_1_VAL, value)

        if self.POT_2_VAL in msg:
            value = int(msg.split("-")[1])
            if value != self.pot_2:
                self.pot_2 = value
                self._pot_handlers[self.POT_2_VAL](self.POT_2_VAL, value)

    def set_button_handler(self, button, handler):
        """Set a handler for a button"""
        if button in self._button_handlers:
            self._button_handlers[button] = handler

    def set_switch_handler(self, switch, handler):
        """Set a handler for a switch"""
        if switch in self._switch_handlers:
            self._switch_handlers[switch] = handler

    def set_channel_handler(self, channel, handler):
        """Set a handler for a channel switch"""
        if channel in self._channel_handlers:
            self._channel_handlers[channel] = handler

    def set_pot_handler(self, pot, handler):
        """Set a handler for a pot"""
        if pot in self._pot_handlers:
            self._pot_handlers[pot] = handler

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
