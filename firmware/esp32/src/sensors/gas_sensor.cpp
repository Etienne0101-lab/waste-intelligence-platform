#include "gas_sensor.h"

const int GAS_SENSOR_PIN = 34;
const float CONTAMINATION_THRESHOLD = 200.0f;

void initGasSensor() {
  pinMode(GAS_SENSOR_PIN, INPUT);
}

float readContaminationLevel() {
  // Analog read from gas/odor sensor
  int raw = analogRead(GAS_SENSOR_PIN);
  return (float)raw / 4095.0f * 1000.0f;  // Convert to ppm equivalent
}

bool isContaminated() {
  return readContaminationLevel() > CONTAMINATION_THRESHOLD;
}
