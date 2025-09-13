#include <Arduino.h>
#if defined(ESP32)
#include <WiFi.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID "APP"
#define WIFI_PASSWORD "12345678"

#define API_KEY "AIzaSyAyCN5zxHcI3nh_ur-4WUbPrNpRReEJlio"

#define DATABASE_URL "https://ar-project-63c75-default-rtdb.firebaseio.com/monitoring"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
bool signupOK = false;

bool fromFlag = false;
bool toFlag = false;
bool locationFlag = false;
bool percentFlag = false;
bool tempFlag = false;

String temp = "", To = "", BPM = "", heart = "", gyro = "", ab = "";

void setup() {
  Serial.begin(9600);
  connectToWiFi();

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase signup successful");
    signupOK = true;
  } else {
    Serial.printf("Firebase signup error: %s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  readSerialData();

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    updateFirebaseData();
  }
  delay(2500);
}

void connectToWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > 15000) { // Timeout after 15 seconds
      Serial.println("Failed to connect to Wi-Fi.");
      return;
    }
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
}

void readSerialData() {
  while (Serial.available() > 0) {
    char inchar = Serial.read();
    Serial.println("Inchar:" + String(inchar));
    if (inchar == '*') {
      temp = readUntil('#');
      fromFlag = true;
    } else if (inchar == '@') {
      BPM = readUntil('#');
      toFlag = true;
    } else if (inchar == '$') {
      ab = readUntil('#');
      locationFlag = true;
    } else if (inchar == '&') {
      gyro = readUntil('#');
      percentFlag = true;
    } else if (inchar == ')') {
      heart = readUntil('#');
      tempFlag = true;
    }
  }
}

void updateFirebaseData() {
  if (fromFlag) {
    fromFlag = false;
    updateFirebase("monitoring/temperature", temp);
  }

  if (toFlag) {
    toFlag = false;
    updateFirebase("monitoring/BPM", BPM);
  }

  if (locationFlag) {
    locationFlag = false;
    updateFirebase("monitoring/abnormal", ab);
  }

  if (percentFlag) {
    percentFlag = false;
    updateFirebase("monitoring/gyro", gyro);
  }

  if (tempFlag) {
    tempFlag = false;
    updateFirebase("monitoring/heart", heart);
  }
}

String readUntil(char terminator) {
  String result = "";
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == terminator) {
      break;
    }
    result += c;
  }
  return result;
}

void updateFirebase(String path, String value) {
  if (Firebase.RTDB.setString(&fbdo, path, value)) {
    Serial.println("PASSED: " + path);
    Serial.println("Value: " + value);
  } else {
    Serial.println("FAILED to update " + path);
    Serial.println("Reason: " + fbdo.errorReason());
  }
}
