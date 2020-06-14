#include <LiquidCrystal.h>
#include "pitches.h"

const int trigPin = A1;
const int echoPin = A0;
long duration;
int distance;

const int buzzer = A5;
const int delayTime = 130;
const int interval = 7;
int noteToPlay;
String noteToSend;

const int button = 2;
int index = 0;


int melody[] = {/*NOTE_E4, NOTE_F4,NOTE_G4,NOTE_C5, 0,NOTE_AS4, NOTE_AS4, NOTE_A4, NOTE_G4,0, */NOTE_AS4,NOTE_AS4,NOTE_A4,NOTE_A4,NOTE_G4,NOTE_G4, NOTE_A4, 0, NOTE_C4, 0, NOTE_C4, 0, NOTE_C4};
int noteDurations[] = { /*4, 8, 4, 8, 2, 4, 8, 4, 8, 2,*/ 4, 8, 4, 8, 4, 8, 8, 6, 6, 6, 6, 6, 6};

int note[8] = {NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_C5};
String notes[8] = {"C4","D4","E4","F4","G4","A4","B4","C5"};
String mode[] = {"Portable Mode", "instrument Mode"};

LiquidCrystal lcd(4, 5, 6, 7, 8, 9);

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(button, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button), cycle, FALLING);
  Serial.begin(9600);

  lcd.setCursor(0, 0);
  lcd.print("Mode Select:");
  lcd.setCursor(0, 1);
  lcd.print(mode[index]);

  for (int thisNote = 0; thisNote < 13; thisNote++) {

    int noteDuration = 1000 / noteDurations[thisNote];
    tone(buzzer, melody[thisNote], noteDuration);

    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(buzzer);
  }

}

void loop() {
  distance = 200;
  while (distance > 5) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2000);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance  = duration / 29 / 2;
    delay(500);
  }
  if (index == 0) {
    portable();
  }
  else {
    instrument();
  }
}

void cycle() {
  if (index == 1) {
    index = 0;
  }
  else {
    index++;
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Mode Select:");
  lcd.setCursor(0, 1);
  lcd.print(mode[index]);

}

void instrument() {
  lcd.clear();
  lcd.print("now in inst mode");
  noTone(buzzer);
  detachInterrupt(digitalPinToInterrupt(button));
  while (true) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2000);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance  = duration / 29 / 2;
    if (interval * 0 < distance && distance <= interval * 1) {
      noteToSend = notes[0];
    }
    else if (interval * 1 < distance && distance <= interval * 2) {
      noteToSend = notes[1];
    }
    else if (interval * 2.5 < distance && distance <= interval * 3) {
      noteToSend = notes[2];
    }
    else if (interval * 3.5 < distance && distance <= interval * 4) {
      noteToSend = notes[3];
    }
    else if (interval * 4.5 < distance && distance <= interval * 5) {
      noteToSend = notes[4];
    }
    else if (interval * 5.5 < distance && distance <= interval * 6) {
      noteToSend = notes[5];
    }
    else if (interval * 6.5 < distance && distance <= interval * 7) {
      noteToSend = notes[6];
    }
    else if (interval * 7.5 < distance && distance <= interval * 8) {
      noteToSend = "H";
    }
    else {
      noteToSend = "0";
    }
    if (noteToSend != "0" ) {
      Serial.println(noteToSend);
      delay(500);
    }
  }
}
void portable() {
  lcd.clear();
  lcd.print("now in port mode");
  detachInterrupt(digitalPinToInterrupt(button));
  while (true) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2000);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance  = duration / 29 / 2;
    if (interval * 0 < distance && distance <= interval * 1) {
      noteToPlay = note[0];
    }
    else if (interval * 1 < distance && distance <= interval * 2) {
      noteToPlay = note[1];
    }
    else if (interval * 2.5 < distance && distance <= interval * 3) {
      noteToPlay = note[2];
    }
    else if (interval * 3.5 < distance && distance <= interval * 4) {
      noteToPlay = note[3];
    }
    else if (interval * 4.5 < distance && distance <= interval * 5) {
      noteToPlay = note[4];
    }
    else if (interval * 5.5 < distance && distance <= interval * 6) {
      noteToPlay = note[5];
    }
    else if (interval * 6.5 < distance && distance <= interval * 7) {
      noteToPlay = note[6];
    }
    else if (interval * 7.5 < distance && distance <= interval * 8) {
      noteToPlay = note[7];
    }
    else {
      noteToPlay = 0;
    }
    if (noteToPlay != 0 ) {
      tone(buzzer, noteToPlay, 200);
      delay(100);
    }
    else {
      noTone(buzzer);
    }
  }
}
