#include <WiFiClient.h>
#include <PubSubClient.h>

#include "mqtt_client.h"

namespace {
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
const char* MQTT_BROKER = "mqtt.local";
const uint16_t MQTT_PORT = 1883;
const char* MQTT_TOPIC = "waste/bin/telemetry";
}

void mqttClientBegin() {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
}

void mqttLoop() {
  if (!mqttClient.connected()) {
    // In production, use environment-driven credentials and retry logic.
    Serial.println("MQTT reconnect attempt");
    mqttClient.connect("esp32-bin-001");
  }
  mqttClient.loop();
}

void publishTelemetry(const String& payload) {
  mqttClient.publish(MQTT_TOPIC, payload.c_str());
}
