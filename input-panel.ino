const int S_SW1_PIN = 11;
const int S_SW2_PIN = 10;

const int CTRL_LED_PIN = 9;
const int CTRL_BT_PIN = 8; // doesnt seem to want to work

const int BT1_PIN = 7; // doesnt seem to want to work
const int BT2_PIN = 6; // doesnt seem to want to work
const int BT3_PIN = 5; // doesnt seem to want to work
const int BT4_PIN = 4; // doesnt seem to want to work

const int P_SW1_PIN = 16;
const int P_SW2_PIN = 17;
const int P_SW3_PIN = 18;
const int P_SW4_PIN = 19;
const int P_SW5_PIN = 20;
const int P_SW6_PIN = 21;
const int P_SW7_PIN = 3;
const int P_SW8_PIN = 2;

const int K1_PIN = A0; // doesnt seem to want to work
const int K2_PIN = A1; // doesnt seem to want to work

void setup() {
  Serial.begin(9600);
  
  pinMode(S_SW1_PIN, INPUT_PULLUP);
  pinMode(S_SW2_PIN, INPUT_PULLUP);

  pinMode(CTRL_LED_PIN, OUTPUT);
  // pinMode(CTRL_BT_PIN, INPUT);

  // pinMode(BT1_PIN, INPUT_PULLUP);
  // pinMode(BT2_PIN, INPUT_PULLUP);
  // pinMode(BT3_PIN, INPUT_PULLUP);
  // pinMode(BT4_PIN, INPUT_PULLUP);

  pinMode(P_SW1_PIN, INPUT_PULLUP);
  pinMode(P_SW2_PIN, INPUT_PULLUP);
  pinMode(P_SW3_PIN, INPUT_PULLUP);
  pinMode(P_SW4_PIN, INPUT_PULLUP);
  pinMode(P_SW5_PIN, INPUT_PULLUP);
  pinMode(P_SW6_PIN, INPUT_PULLUP);
  pinMode(P_SW7_PIN, INPUT_PULLUP);
  pinMode(P_SW8_PIN, INPUT_PULLUP);

  digitalWrite(CTRL_LED_PIN, LOW);
}

void loop() {

  int potVal1 = analogRead(K1_PIN);
  int potVal2 = analogRead(K2_PIN);
  Serial.println(potVal2);
  // Serial.println(String(digitalRead(P_SW1_PIN)) + String(digitalRead(P_SW2_PIN)) + String(digitalRead(P_SW3_PIN)) +
  // String(digitalRead(P_SW4_PIN)) + String(digitalRead(P_SW5_PIN)) + String(digitalRead(P_SW6_PIN)) +
  // String(digitalRead(P_SW7_PIN)) + String(digitalRead(P_SW8_PIN)));
  delay(10);
}
