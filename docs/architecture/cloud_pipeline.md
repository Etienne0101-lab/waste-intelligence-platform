# Cloud Pipeline

The cloud layer coordinates ingestion, analytics, mapping, and reporting.

## Ingestion paths

- MQTT broker integration
- LoRaWAN uplink validation
- Hub-synchronized facility feeds
- Async batch ingestion for historical snapshots

## Data storage

- PostgreSQL with TimescaleDB for time-series workloads
- Event and telemetry tables for bins, clusters, and facilities

## Analytics

- Temporal histograms for hourly and daily patterns
- Spatial histograms for block, neighborhood, and borough summaries
- Forecasting for diversion, overflow, and facility load

## Dashboards

- Streamlit for interactive operational dashboards
- Grafana for live metrics and monitoring views
