#include <SoftwareSerial.h>
SoftwareSerial serial(6, 7);//rx tx
#include <LiquidCrystal.h>
LiquidCrystal lcd(13, 12, 11, 10, 9, 8);
#include "DHT.h"
#define DHTPIN 2

#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int t;
int BPM;
char Data = 'x';
void setup() {
  Serial.begin(9600);
  serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Heart - Health");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring");
  pinMode(4, INPUT); // Setup for leads off detection LO +
  pinMode(3, INPUT);
  delay(1000);
  lcd.clear();
}

void loop() {
  Data = 'x';
  serialEvent();
  t = dht.readTemperature();
  //  Serial.println("t:" + String(t));
  if ((digitalRead(3) == 1) || (digitalRead(4) == 1)) {
    //    Serial.println('!');
  }
  else {
    BPM = analogRead(A0);
    //    Serial.println("BPM:" + String(BPM));
  }
  send_fire("*" + String(t) + "#");
  send_fire("@" + String(BPM) + "#");

  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.setCursor(2, 0);
  lcd.print(String(t) + "                    ");
  lcd.setCursor(0, 1);
  lcd.print("BPM:");
  lcd.setCursor(4, 1);
  lcd.print(String(BPM) + "                    ");
  delay(1000);
}

void send_fire(String s)
{
  for (int i = 0; i < s.length(); i++)
  {
    serial.write(s[i]);
  }
  delay(2000);
}

void python(String s)
{
  for (int i = 0; i < s.length(); i++)
  {
    Serial.write(s[i]);
  }
  delay(1000);
}

void serialEvent()
{
  while (Serial.available() > 0)
  {
    Data = Serial.read();
  }
  switch (Data)
  {
    case 'A':
      lcd.setCursor(0, 0);
      lcd.print("Heart Attack           ");
      lcd.setCursor(0, 1);
      lcd.print("Likely..               ");
      send_fire("$Heart Attack Likely#");
      Data = 'x';
      break;

    case 'B':
      lcd.setCursor(0, 0);
      lcd.print("No chance              ");
      lcd.setCursor(0, 1);
      lcd.print("Heart Attack              ");
      send_fire("$No chance Heart Attack#");
      Data = 'x';
      break;
    case 'C':
      lcd.setCursor(0, 0);
      lcd.print("Requesting..          ");
      python("*" + String(BPM) + "#$");
      lcd.setCursor(0, 0);
      lcd.print("Data Send..          ");
      break;
  }
}
