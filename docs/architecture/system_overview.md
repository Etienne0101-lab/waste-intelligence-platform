# Architecture Overview

This document describes the layered platform architecture used across the waste-intelligence system.

## Layered model

### Sensor layer
The sensor layer is responsible for capturing waste volume, mass, contamination indicators, and telemetry timestamps. It connects to mesh gateways and the wider network using ESP32-based hardware.

### Mesh layer
Bins form local clusters that aggregate telemetry before forwarding to a facility or central system. This creates resilience and reduces network load.

### Hub layer
Facilities act as regional aggregation points. They validate data, compute route recommendations, and forecast facility load based on current and historical telemetry.

### Cloud layer
The cloud layer stores telemetry in Postgres/TimescaleDB, runs predictive analytics, generates spatial maps, and powers dashboards for DSNY and agency stakeholders.

## Operational principles

- Local inference at the mesh edge
- Downstream normalization before cloud storage
- Event-driven processing when possible
- Secure configuration via environment variables
- Explicit data ownership and traceability
