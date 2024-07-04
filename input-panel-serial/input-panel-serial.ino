// Version 0.1
const int S_SW1_PIN = 8;
const int S_SW2_PIN = 7;

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

const int K1_PIN = A1;
const int K2_PIN = A0;

int scalePotValue(int potValue) {
  return 100 - map(potValue, 0, 1023, 0, 100);
}

void setup() {
  Serial.begin(9600);
  
  pinMode(S_SW1_PIN, INPUT_PULLUP);
  pinMode(S_SW2_PIN, INPUT_PULLUP);

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

  digitalWrite(CTRL_LED_PIN, LOW);
}

void loop() {

  int potVal1 = analogRead(K1_PIN);
  int potVal2 = analogRead(K2_PIN);

  // Pass channel
  Serial.print(String(!digitalRead(CH_SW1_PIN)) + String(!digitalRead(CH_SW2_PIN)) + String(!digitalRead(CH_SW3_PIN)) + String(!digitalRead(CH_SW4_PIN)) + "-");
  
  // Pass switch states
  Serial.print(String(!digitalRead(S_SW1_PIN)) + String(!digitalRead(S_SW2_PIN)) + "-");

  // Pass button press
  Serial.print(String(!digitalRead(BT1_PIN)) + String(!digitalRead(BT2_PIN)) + String(!digitalRead(BT3_PIN)) + String(!digitalRead(BT4_PIN)) + String(!digitalRead(CTRL_BT_PIN)) + "-");

  // Pass pot values
  Serial.println(String(scalePotValue(potVal1)) + "-" + String(scalePotValue(potVal2)));
  

  if (digitalRead(S_SW1_PIN) == 0 && digitalRead(S_SW2_PIN) == 0) {
    digitalWrite(CTRL_LED_PIN, HIGH);
  } else {
    digitalWrite(CTRL_LED_PIN, LOW);
  }
  delay(25);
}
