#pragma once

#include <Arduino.h>

void initPowerManagement();
void goToDeepSleep(uint32_t sleep_seconds);
float getBatteryVoltage();
bool isBatteryLow();
