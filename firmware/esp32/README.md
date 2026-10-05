# ESP32 Sensor Firmware

Production-grade firmware for sensor-enabled waste bins with MQTT, LoRaWAN, and BLE-Mesh support.

## Sensor stack

- Ultrasonic fill-level detection (HC-SR04 or equivalent)
- Load-cell mass measurement (HX711 ADC)
- Gas/contamination sensor (MQ series or equivalent)
- Battery voltage monitoring

## Connectivity options

- MQTT over WiFi
- LoRaWAN uplink
- BLE-Mesh local clustering
- Fallback to local storage when disconnected

## Build and deployment

```bash
cd firmware/esp32
pio run
pio run -t upload
```

## Configuration

Sensor pins and calibration constants are defined in header files and can be overridden via environment or EEPROM.

## Testing

Run hardware-in-the-loop tests to validate sensor readings and connectivity:

```bash
pio test
```
