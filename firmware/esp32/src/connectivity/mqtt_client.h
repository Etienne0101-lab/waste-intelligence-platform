#pragma once

#include <Arduino.h>

void mqttClientBegin();
void mqttLoop();
void publishTelemetry(const String& payload);
