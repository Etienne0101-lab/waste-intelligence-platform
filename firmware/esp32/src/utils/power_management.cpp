#include "power_management.h"

const int BATTERY_ADC_PIN = 35;
const float BATTERY_DIVIDER = 2.0f;
const float BATTERY_LOW_THRESHOLD = 3.0f;  // Volts

void initPowerManagement() {
  pinMode(BATTERY_ADC_PIN, INPUT);
}

void goToDeepSleep(uint32_t sleep_seconds) {
  esp_sleep_enable_timer_wakeup(sleep_seconds * 1000000ULL);
  esp_deep_sleep_start();
}

float getBatteryVoltage() {
  int raw = analogRead(BATTERY_ADC_PIN);
  float vref = 3.3f;
  return (raw / 4095.0f) * vref * BATTERY_DIVIDER;
}

bool isBatteryLow() {
  return getBatteryVoltage() < BATTERY_LOW_THRESHOLD;
}
