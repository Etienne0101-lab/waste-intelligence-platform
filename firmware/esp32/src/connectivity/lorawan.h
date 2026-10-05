#pragma once

#include <Arduino.h>

void initLoRaWAN();
void sendLoRaPacket(const String& payload);
bool isLoRaConnected();
uint8_t getLoRaSignalStrength();
