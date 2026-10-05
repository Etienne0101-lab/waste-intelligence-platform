#include "calibration.h"
#include <EEPROM.h>

const int EEPROM_CAL_ADDR = 0;
const int EEPROM_SIZE = 512;

void storeCalibration(const CalibrationData& cal) {
  EEPROM.begin(EEPROM_SIZE);
  EEPROM.put(EEPROM_CAL_ADDR, cal);
  EEPROM.commit();
  EEPROM.end();
}

CalibrationData loadCalibration() {
  CalibrationData cal = {0.0f, 1.0f, 2280.0f, 0};
  EEPROM.begin(EEPROM_SIZE);
  EEPROM.get(EEPROM_CAL_ADDR, cal);
  EEPROM.end();
  return cal;
}

float applyCalibratedFillLevel(float raw_distance_cm) {
  CalibrationData cal = loadCalibration();
  float adjusted = (raw_distance_cm - cal.fill_zero_offset) * cal.fill_span_factor;
  return constrain(adjusted, 0.0f, 100.0f);
}
