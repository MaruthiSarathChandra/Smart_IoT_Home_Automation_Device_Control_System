#include "DeviceRegistry.h"
#include <vector>

Device DeviceRegistry::devices[MAX_DEVICES];

void DeviceRegistry::initDevices() {

  // SLOT 1
  devices[0] = { 1, "PIR", false, 22, 0, DIGITAL, true , false};

  // SLOT 2
  devices[1] = { 2, "LDR", false, 34, 0, ANALOG_INPUT,  true, false};

  // SLOT 3
  devices[2] = { 3, "LED", false, 15, 0, PWM, false, false};

  // SLOT 4
  devices[3] = { 4, "BUZZER", false, 2, 0, DIGITAL, false, false};

  // SLOT 5
  devices[4] = { 5, "x", false, 27, 19, DIGITAL, false, false};

  // SLOT 6
  devices[5] = { 6, "", false, -1, 21, DIGITAL, false, false};

  // SLOT 7
  devices[6] = { 7, "", false, -1, 13, DIGITAL, false, false};

  // SLOT 8
  devices[7] = { 8, "", false, -1, 26, DIGITAL, false, false};

  // SLOT 9
  devices[8] = { 9, "", false, -1, 27, DIGITAL, false, false};

  // SLOT 10
  devices[9] = { 10, "", false, -1, 14, DIGITAL, false, false};


}

String DeviceRegistry::updateDevice(int device_id, int value) {

  int index = device_id - 1;
  if (index < 0 || index >= MAX_DEVICES)
    return "{\"error\":\"Invalid device id\"}";

  if (devices[index].is_read_only)
    return "{\"error\":\"Device is read-only\"}";

  devices[index].value = value;
  devices[index].state = (value > 0);
  devices[index].is_manual_override = true;

  int pin = devices[index].gpio_pin;
  if (pin == -1)
    return "{\"status\":\"updated (virtual)\"}";

  if (devices[index].control_type == DIGITAL) {
    digitalWrite(pin, value > 0 ? HIGH : LOW);
  }
  else if (devices[index].control_type == PWM) {
    analogWrite(pin, value);
  }


  return "{\"status\":\"updated\"}";
}






Device DeviceRegistry::getDevice(int device_id) {
  return devices[device_id - 1];
}





String DeviceRegistry::registerDevice(int device_id, String device_type, bool is_read) {

  int index = device_id - 1;
  if (index < 0 || index >= MAX_DEVICES)
    return "{\"error\":\"invalid device id\"}";

  Serial.println("entered");
  devices[index].type = device_type;
  devices[index].state = true;
  devices[index].value = 0;
  devices[index].is_read_only = is_read;

  return "{\"status\":\"registered\",\"device_id\":" + String(device_id) + "}";
}

void DeviceRegistry::unregisterDevice(int device_id) {

  int index = device_id - 1;
  if (index < 0 || index >= MAX_DEVICES) return;

  devices[index].type = "";
  devices[index].state = false;
  devices[index].value = 0;

}

String DeviceRegistry::getAllDevicesAsJson() {

  String json = "[";

  for (int i = 0; i < MAX_DEVICES; i++) {

    json += "{";
    json += "\"device_id\":" + String(devices[i].device_id) + ",";
    json += "\"type\":\"" + devices[i].type + "\",";
    json += "\"state\":" + String(devices[i].state ? "true" : "false") + ",";
    json += "\"gpio_pin\":" + String(devices[i].gpio_pin) + ",";
    json += "\"value\":" + String(devices[i].value) + ",";
    json += "\"control_type\":" + String(devices[i].control_type) + ",";
    json += "\"is_read_only\":" + String(devices[i].is_read_only ? "true" : "false");
    json += "}";

    if (i < MAX_DEVICES - 1) json += ",";
  }

  json += "]";
  return json;
}

String DeviceRegistry::getNextAvailableDeviceId() {

  String json = "{\"available_device_ids\": [";
  bool first = true;

  for (int i = 0; i < MAX_DEVICES; i++) {

    // state == false AND type == ""
    if (devices[i].state == false && devices[i].type == "") {

      if (!first) json += ",";
      first = false;

      json += String(devices[i].device_id);
    }
  }

  json += "] }";
  return json;
}





