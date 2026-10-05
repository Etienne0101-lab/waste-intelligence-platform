# Platform Overview

This project implements a distributed IoT mesh waste-intelligence platform for organic waste monitoring, diversion analytics, routing optimization, and city-scale operational intelligence.

## System layers

1. Sensor Layer
   - ESP32-enabled bins with ultrasonic and load-cell sensing
   - MQTT, LoRaWAN, BLE-Mesh uplink
   - Battery management and calibration logic

2. Mesh Layer
   - MQTT broker, LoRaWAN server, and Node-RED aggregation
   - Packet normalization and cluster synchronization

3. Hub Layer
   - Flask-based API and regional facility logic
   - Haversine routing and facility forecasting

4. Cloud Layer
   - Ingestion, analytics, mapping, and dashboard services
   - Predictive modeling and histographic analysis

5. DevOps Layer
   - Docker Compose orchestration
   - Prometheus and Grafana monitoring
   - GitHub Actions CI/CD

## Data flow

Sensor -> Mesh -> Hub -> Cloud -> Analytics -> Dashboards -> NYC agencies

## Design goals

- Real-time operational visibility
- Auditable diversion metrics
- Optimized facility routing and forecasting
- Multi-scale mapping from building to borough
- Safe and secure cloud deployment using environment variables and access controls
