#include <WiFi.h>
#include <WebServer.h>

#include "DeviceRegistry.h"
#include "RestApiServer.h"

//  WiFi Credentials
#define WIFI_SSID     //WIFI_USER_ID
#define WIFI_PASSWORD //WIFI_PASSWORD

//  Device IDs
#define PIR_DEVICE_ID      1
#define LIGHT_DEVICE_ID    3
#define BUZZER_DEVICE_ID   4
#define RESERVED_DEVICE_ID 2
#define LDR_GPIO 34


bool pir_has_control = true;   // PIR controls devices by default
bool light_locked = false;    // Prevent repeated updates
unsigned long lastPirCheck = 0;
const unsigned long PIR_INTERVAL = 500; // 0.5 second check interval


WebServer server(80);

void setup() {
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n WiFi Connected!");
  Serial.print(" ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  //  Initialize Registry + GPIO + PWM
  DeviceRegistry::initDevices();

  //  Configure PIR INPUT
  pinMode(DeviceRegistry::getDevice(PIR_DEVICE_ID).gpio_pin, INPUT);

  //  Configure Light + Buzzer OUTPUT
  pinMode(DeviceRegistry::getDevice(LIGHT_DEVICE_ID).gpio_pin, OUTPUT);
  pinMode(DeviceRegistry::getDevice(BUZZER_DEVICE_ID).gpio_pin, OUTPUT);

  startRestServer(server);
  server.begin();
}



// ✅ Run automation every 300 ms (not every CPU cycle)
unsigned long lastAutomationTime = 0;
const unsigned long AUTOMATION_INTERVAL = 300;   // milliseconds

void loop() {


  // ✅ ALWAYS keep server responsive (FAST)
  server.handleClient();

  // ✅ NON-BLOCKING TIME CHECK
  unsigned long now = millis();
  if (now - lastAutomationTime < AUTOMATION_INTERVAL) {
    return;   // 🔥 This prevents "bullet speed"
  }
  lastAutomationTime = now;

  // ✅ Get devices
  Device pirDevice    = DeviceRegistry::getDevice(PIR_DEVICE_ID);
  Device lightDevice  = DeviceRegistry::getDevice(LIGHT_DEVICE_ID);
  Device buzzerDevice = DeviceRegistry::getDevice(BUZZER_DEVICE_ID);

  //  Read sensors
  int pirValue = digitalRead(pirDevice.gpio_pin);
  int ldrValue = analogRead(LDR_GPIO);

  //Serial.print("PIR: ");
  //Serial.print(pirValue);
  //Serial.print(" | LDR: ");
  //Serial.println(ldrValue);

  //  MANUAL OVERRIDE CHECK (FLASK HAS PRIORITY)
  if (lightDevice.is_manual_override == true) {
    return;   // ESP32 automation PAUSED
  }

  //  NIGHT LOGIC
  bool isNight = (ldrValue > 2000);   // adjust threshold later

  //  AUTO ON
  if (pirValue == HIGH && isNight) {

    if (lightDevice.state == false) {
      DeviceRegistry::updateDevice(LIGHT_DEVICE_ID, 255);
      DeviceRegistry::updateDevice(BUZZER_DEVICE_ID, HIGH);
      Serial.println("AUTO: Light & Buzzer ON");
    }
  }

  //  AUTO OFF
  else if (pirValue == LOW) {

    if (lightDevice.state == true) {
      DeviceRegistry::updateDevice(LIGHT_DEVICE_ID, 0);
      DeviceRegistry::updateDevice(BUZZER_DEVICE_ID, 0);
      Serial.println("AUTO: Light & Buzzer OFF");
    }
  }
}
