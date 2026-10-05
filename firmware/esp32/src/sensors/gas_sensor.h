#pragma once

#include <Arduino.h>

void initGasSensor();
float readContaminationLevel();
bool isContaminated();
