# Mesh Cluster Setup

## Topology

Each cluster consists of:
- 1 Mosquitto MQTT broker (or gateway)
- Multiple sensor nodes publishing to local topics
- Optional Node-RED orchestrator for packet enrichment

## Topic structure

```
waste/
  bin/
    <bin-id>/telemetry
    <bin-id>/status
  cluster/
    <cluster-id>/aggregate
    <cluster-id>/health
  facility/
    <facility-id>/dispatch
    <facility-id>/forecast
```

## Deployment

### Docker Compose (local development)

```yaml
services:
  mqtt:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
```

### Production notes

- Enable persistent storage
- Use TLS with valid certificates
- Restrict anonymous access
- Monitor broker memory and message throughput
