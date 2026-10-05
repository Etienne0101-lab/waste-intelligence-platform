# Distributed IoT Mesh Waste-Intelligence Platform

A production-ready distributed IoT platform for real-time organic waste intelligence across NYC buildings, blocks, and facilities.

## Architecture summary

The platform follows a Hub-and-Spoke model:
- Spokes: sensor-enabled waste bins
- Mesh clusters: building/block aggregation nodes
- Hubs: composting, recycling, and remediation facilities
- Cloud: ingestion, storage, analytics, mapping, dashboards

Data flow:
- Sensor → Mesh → Hub → Cloud → Analytics → Dashboards → NYC agencies

## Repository structure

- `firmware/` — ESP32 sensor firmware and hardware tests
- `mesh-network/` — MQTT, LoRaWAN, Node-RED, and normalization utilities
- `hub-layer/` — Flask API and regional forecasting logic
- `cloud-platform/` — ingestion, analytics, dashboards, and mapping pipelines
- `devops/` — Docker, CI/CD, Prometheus, Grafana
- `docs/` — architecture, deployment, and diagram docs
- `scripts/` — operational automation for environment setup and data pipelines

## Key technologies

- ESP32 C++ firmware
- MQTT, LoRaWAN, BLE-Mesh connectivity
- Flask API layer
- Python ingestion and analytics services
- Postgres/TimescaleDB storage
- Streamlit + Grafana dashboards
- Docker Compose orchestration
- GitHub Actions CI/CD

## Quick start

1. Clone the repository
2. Copy environment values into a `.env` file
3. Start the base stack with Docker Compose
4. Run the API and Streamlit apps
5. Deploy the ESP32 firmware through PlatformIO

## Security

- Secrets must be stored in environment variables
- Use TLS for MQTT and API traffic in production
- Restrict cloud access via authentication and least privilege

## Contributing

See `CONTRIBUTING.md` for contribution guidelines.

## License

This project is distributed under the MIT License. See `LICENSE`.
