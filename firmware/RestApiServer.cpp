#include "RestApiServer.h"
#include "DeviceRegistry.h"
#include <ArduinoJson.h>

void startRestServer(WebServer &server) {

  server.on("/devices", HTTP_GET, [&](){
    server.send(200, "application/json", DeviceRegistry::getAllDevicesAsJson());
  });



  //------------ GETTER AVAILABLE DEVICE_IDs ------------
  server.on("/devices/available", HTTP_GET, [&](){

    String json = DeviceRegistry::getNextAvailableDeviceId();
    Serial.print("sendback");
    server.send(200, "application/json", json);
  });


  //------------ SETTER DEVICE's ------------
  server.on("/devices/register", HTTP_POST, [&](){

    StaticJsonDocument<200> doc;
    deserializeJson(doc, server.arg("plain"));

    int id = doc["device_id"];
    String type = doc["type"].as<String>();
    bool is_read = doc["is_read"].as<bool>();
    Serial.println(is_read);

    String res = DeviceRegistry::registerDevice(id, type, is_read);
    server.send(200, "application/json", res);
  });

  //------------ SETTER DEVICE's ------------
  server.on("/devices/set", HTTP_POST, [&](){

    StaticJsonDocument<200> doc;
    deserializeJson(doc, server.arg("plain"));

    int id = doc["device_id"];
    Serial.print("id------>");
    Serial.println(id);
    int value = doc["data_value"];

    String result = DeviceRegistry::updateDevice(id, value);
    server.send(200, "application/json", result);
  });


  //------------ DELETE DEVICE's ------------
  server.on("/devices/delete", HTTP_POST, [&](){

    StaticJsonDocument<200> doc;
    deserializeJson(doc, server.arg("plain"));

    int id = doc["device_id"];
    DeviceRegistry::unregisterDevice(id);

    server.send(200, "application/json", "{\"status\":\"deleted\"}");
  });


  //------------ GETTER DEVICE's ------------
  server.on("/devices/get", HTTP_POST, [&]() {

    StaticJsonDocument<200> doc;
    deserializeJson(doc, server.arg("plain"));

    int id = doc["device_id"];
    Device d = DeviceRegistry::getDevice(id);

    String json = "{";
    json += "\"device_id\":" + String(d.device_id) + ",";
    json += "\"type\":\"" + d.type + "\",";
    json += "\"state\":" + String(d.state ? "true" : "false") + ",";
    json += "\"gpio_pin\":" + String(d.gpio_pin) + ",";
    json += "\"value\":" + String(d.value) + ",";
    json += "\"is_read_only\":" + String(d.is_read_only ? "true" : "false");
    json += "}";

    server.send(200, "application/json", json);
  });


}
