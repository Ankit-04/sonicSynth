#include <LiquidCrystal.h>
#include "pitches.h"

bool hasStartedPortable = false;
bool hasStartedInstrument = false;
int lastNote;
const int trigPin = 11;
const int echoPin = 12;
const int buzzer = 10;
const int button = 2;
long duration;
int distance;
int index = 0;
int melody[] = {NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4};
int noteDurations[] = { 4, 8, 8, 4, 4, 4, 4, 4};

int note[8] = {NOTE_C4, NOTE_DS4, NOTE_F4, NOTE_FS4, NOTE_G4, NOTE_AS4, NOTE_C5, NOTE_DS5};
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

  for (int thisNote = 0; thisNote < 8; thisNote++) {

    int noteDuration = 1000 / noteDurations[thisNote];
    tone(buzzer, melody[thisNote], noteDuration);

    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(buzzer);
  }

}
void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2000);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance  = duration / 29 / 2;
  delay(500);

  if(distance < 5){
    hasStartedPortable = true;
  }
  if (index == 0 && hasStartedPortable) {
    portable(distance);
  }
  else if(index == 1 && hasStartedInstrument){
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

void portable(int distance) {
  int noteToPlay;
  if (10 < distance && distance <= 19) {
    noteToPlay = note[0];
  }
  else if (19 < distance && distance <= 26) {
    noteToPlay = note[1];
  }
  else if (26 < distance && distance <= 33) {
    noteToPlay = note[2];
  }
  else if (33 < distance && distance <= 40) {
    noteToPlay = note[3];
  }
  else if (40 < distance && distance <= 47) {
    noteToPlay = note[4];
  }
  else if (47 < distance && distance <= 54) {
    noteToPlay = note[5];
  }
  else if (54 < distance && distance <= 61) {
    noteToPlay = note[6];
  }
  else if (61 < distance && distance <= 68) {
    noteToPlay = note[7];
  }
  else {
    lastNote = NULL;
  }
  if (noteToPlay != NULL && noteToPlay != lastNote) {
    tone(buzzer, noteToPlay, 500);
  }
  else {
    noTone(buzzer);
  }
  lastNote = noteToPlay;
}
void instrument() {
  lcd.clear();
  lcd.print("now in inst mode");
  while (true) {

  }
}
