#include "loadcell.h"

// HX711 pinout
const int HX711_DT_PIN = 32;
const int HX711_SCK_PIN = 33;

// Calibration constants
const float CALIBRATION_FACTOR = 2280.0f;  // Adjust per sensor
const float TARE_WEIGHT = 0.0f;

void initLoadCell() {
  pinMode(HX711_DT_PIN, INPUT);
  pinMode(HX711_SCK_PIN, OUTPUT);
  digitalWrite(HX711_SCK_PIN, LOW);
}

float readMassKg() {
  // Placeholder for actual HX711 reading logic
  // In production, integrate adafruit/Adafruit_HX711 or equivalent
  return 18.5f;
}

float getTareWeight() {
  return TARE_WEIGHT;
}

float getCalibrationFactor() {
  return CALIBRATION_FACTOR;
}
