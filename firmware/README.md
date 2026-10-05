# ESP32 Firmware

This folder contains the ESP32 firmware for sensor-enabled bins.

## Responsibilities

- read ultrasonic and load-cell data
- apply calibration and filtering
- package telemetry for MQTT or LoRaWAN uplink
- manage power state and local alerts

## Build

Use PlatformIO:

```bash
pio run
pio run -t upload
```
