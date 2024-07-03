const int S_SW1_PIN = 8;
const int S_SW2_PIN = 7;

const int CTRL_LED_PIN = 2;
const int CTRL_BT_PIN = 17; // BLACK

const int BT1_PIN = 21; // YELLOW
const int BT2_PIN = 19; // WHITE
const int BT3_PIN = 18; // RED
const int BT4_PIN = 16; // BLUE

const int P_SW1_PIN = 12;
const int P_SW2_PIN = 11;
const int P_SW3_PIN = 10;
const int P_SW4_PIN = 9;

const int K1_PIN = A1;
const int K2_PIN = A0;

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

  pinMode(P_SW1_PIN, INPUT_PULLUP);
  pinMode(P_SW2_PIN, INPUT_PULLUP);
  pinMode(P_SW3_PIN, INPUT_PULLUP);
  pinMode(P_SW4_PIN, INPUT_PULLUP);

  digitalWrite(CTRL_LED_PIN, LOW);
}

void loop() {

  int potVal1 = analogRead(K1_PIN);
  int potVal2 = analogRead(K2_PIN);

  Serial.print(String(digitalRead(BT1_PIN)) + String(digitalRead(BT2_PIN)) + String(digitalRead(BT3_PIN)) + String(digitalRead(BT4_PIN)) + String(digitalRead(CTRL_BT_PIN)));
  Serial.print("-" + String(potVal1) + "-" + String(potVal2));
  Serial.print("-" + String(digitalRead(P_SW1_PIN)) + String(digitalRead(P_SW2_PIN)) + String(digitalRead(P_SW3_PIN)) + String(digitalRead(P_SW4_PIN)));
  Serial.println("-" + String(digitalRead(S_SW1_PIN)) + String(digitalRead(S_SW2_PIN)));

  if (digitalRead(S_SW2_PIN) == 0) {
    digitalWrite(CTRL_LED_PIN, HIGH);
  } else {
    digitalWrite(CTRL_LED_PIN, LOW);
  }
  delay(10);
}
