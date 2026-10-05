#pragma once

#include <Arduino.h>

struct CalibrationData {
  float fill_zero_offset;
  float fill_span_factor;
  float mass_calibration_factor;
  uint32_t timestamp;
};

void storeCalibration(const CalibrationData& cal);
CalibrationData loadCalibration();
float applyCalibratedFillLevel(float raw_distance_cm);
