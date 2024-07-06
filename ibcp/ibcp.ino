// Input board communication protocol version 0.1

// Pins
const int SW1_PIN = 8;
const int SW2_PIN = 7;

const int CTRL_LED_PIN = 2;
const int CTRL_BT_PIN = 17; // BLACK

const int BT1_PIN = 21; // YELLOW
const int BT2_PIN = 19; // WHITE
const int BT3_PIN = 18; // RED
const int BT4_PIN = 16; // BLUE

const int CH_SW1_PIN = 12;
const int CH_SW2_PIN = 11;
const int CH_SW3_PIN = 10;
const int CH_SW4_PIN = 9;

const int POT1_PIN = A1;
const int POT2_PIN = A0;

// States
bool CTRL_MODE = false;
bool SW1_ON = false;
bool SW2_ON = false;
bool CH1_ON = false;
bool CH2_ON = false;
bool CH3_ON = false;
bool CH4_ON = false;
int POT1_VAL = 0;
int POT2_VAL = 0;

void initPins() {
  pinMode(SW1_PIN, INPUT_PULLUP);
  pinMode(SW2_PIN, INPUT_PULLUP);

  pinMode(CTRL_LED_PIN, OUTPUT);
  pinMode(CTRL_BT_PIN, INPUT_PULLUP);

  pinMode(BT1_PIN, INPUT_PULLUP);
  pinMode(BT2_PIN, INPUT_PULLUP);
  pinMode(BT3_PIN, INPUT_PULLUP);
  pinMode(BT4_PIN, INPUT_PULLUP);

  pinMode(CH_SW1_PIN, INPUT_PULLUP);
  pinMode(CH_SW2_PIN, INPUT_PULLUP);
  pinMode(CH_SW3_PIN, INPUT_PULLUP);
  pinMode(CH_SW4_PIN, INPUT_PULLUP);
}

void setupInitStates() {
  digitalWrite(CTRL_LED_PIN, LOW);

  SW1_ON = !digitalRead(SW1_PIN);
  SW2_ON = !digitalRead(SW2_PIN);

  CH1_ON = !digitalRead(CH_SW1_PIN);
  CH2_ON = !digitalRead(CH_SW2_PIN);
  CH3_ON = !digitalRead(CH_SW3_PIN);
  CH4_ON = !digitalRead(CH_SW4_PIN);

  POT1_VAL = scalePotValue(analogRead(POT1_PIN));
  POT2_VAL = scalePotValue(analogRead(POT2_PIN));
}

int scalePotValue(int potValue) {
  return 100 - map(potValue, 0, 1023, 0, 100);
}

void invertCtrlButton() {
  CTRL_MODE = !CTRL_MODE;
  digitalWrite(CTRL_LED_PIN, CTRL_MODE);
}

bool handleCtrlButtonPress() {
    if (!digitalRead(CTRL_BT_PIN)) {
        invertCtrlButton();
        delay(300);
    }
}

void handleButtonPress() {
  String msg = String("");

  if (!digitalRead(BT1_PIN)) {
    msg += "B1";
  } else if (!digitalRead(BT2_PIN)) {
    msg += "B2";
  } else if (!digitalRead(BT3_PIN)) {
    msg += "B3";
  } else if (!digitalRead(BT4_PIN)) {
    msg += "B4";
  }

  if (msg.length() == 0) {
    return;
  }

  if (CTRL_MODE) {
    msg += "B";
    invertCtrlButton();
  } else {
    msg += "A";
  }

  Serial.println(msg);
  delay(1000);
}

void handleSwitches() {
  String msg = String("");
  
  bool sw1 = !digitalRead(SW1_PIN);
  bool sw2 = !digitalRead(SW2_PIN);

  if (sw1 != SW1_ON) {
    Serial.println("SW1-" + String(sw1));
    SW1_ON = sw1;
  }

  if (sw2 != SW2_ON) {
    Serial.println("SW2-" + String(sw2));
    SW2_ON = sw2;
  }
}

void handleChannelSwitches() {
  String msg = String("");
  
  bool sw1 = !digitalRead(CH_SW1_PIN);
  bool sw2 = !digitalRead(CH_SW2_PIN);
  bool sw3 = !digitalRead(CH_SW3_PIN);
  bool sw4 = !digitalRead(CH_SW4_PIN);

  if (sw1 != CH1_ON) {
    Serial.println("CH-SW1-" + String(sw1));
    CH1_ON = sw1;
  }

  if (sw2 != CH2_ON) {
    Serial.println("CH-SW2-" + String(sw2));
    CH2_ON = sw2;
  }

  if (sw3 != CH3_ON) {
    Serial.println("CH-SW3-" + String(sw3));
    CH3_ON = sw3;
  }

  if (sw4 != CH4_ON) {
    Serial.println("CH-SW4-" + String(sw4));
    CH4_ON = sw4;
  }
}

void handlePotChange() {
  int pot1  = scalePotValue(analogRead(POT1_PIN));
  int pot2  = scalePotValue(analogRead(POT2_PIN));

  if (pot1 != POT1_VAL) {
    POT1_VAL = pot1;
    Serial.println("POT1-" + String(pot1));
  }

  if (pot2 != POT2_VAL) {
    POT2_VAL = pot2;
    Serial.println("POT2-" + String(pot2));
  }
}

void setup() {
  Serial.begin(9600);
  initPins();
  setupInitStates();
}

void loop() {
  handleCtrlButtonPress();
  handleButtonPress();
  handleSwitches();
  handleChannelSwitches();
  handlePotChange();

  delay(25);
}
