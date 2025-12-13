#ifndef DEVICE_REGISTRY_H
#define DEVICE_REGISTRY_H

#include <Arduino.h>

#define MAX_DEVICES 10

// FIXED ENUM (NO ANALOG NAME)
enum ControlType {
  DIGITAL,
  PWM,
  ANALOG_INPUT
};

struct Device {
  int device_id;
  String type;
  bool state;
  int gpio_pin;
  int value;
  ControlType control_type;
  bool is_read_only;
  bool is_manual_override;   // true if Flask controls it
};

class DeviceRegistry {
public:
  static Device devices[MAX_DEVICES];

  static void initDevices();
  static String updateDevice(int device_id, int value);
  static Device getDevice(int device_id);
  static String getAllDevicesAsJson();
  static String getActiveDevicesAsJson();
  static String registerDevice(int device_id, String device_type, bool is_read);
  static void unregisterDevice(int device_id);


  static String getNextAvailableDeviceId();
};

#endif
