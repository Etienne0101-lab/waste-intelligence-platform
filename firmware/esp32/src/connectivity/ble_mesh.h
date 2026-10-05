#pragma once

#include <Arduino.h>

void initBLEMesh();
void broadcastTelemetry(const String& payload);
bool isMeshConnected();
