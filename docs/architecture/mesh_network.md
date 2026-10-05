# Mesh Network Design

## Objectives

- Self-healing communication between bin nodes and gateways
- Local aggregation before cloud transmission
- Reliable uplink under intermittent connectivity and urban constraints

## Stack

- MQTT for local telemetry and event routing
- LoRaWAN for long-range facility-level connectivity
- BLE-Mesh or mesh-friendly radio patterns for local clustering
- Node-RED for flow orchestration and packet enrichment

## Topology

Each cluster consists of several bins connected to a local aggregator or gateway. The gateway forwards normalized packets to the hub-layer API or cloud service.

## Normalization rules

- Convert raw mass and fill-level values to standard units
- Attach cluster and facility metadata
- Synchronize timestamps across nodes
- Detect missing values and out-of-range readings

## Reliability features

- Reconnection logic for lost brokers or gateways
- Duplicate message suppression
- Retention of local state while upstream connectivity is unavailable
