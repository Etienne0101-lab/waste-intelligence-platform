# MQTT Configuration

Mosquitto MQTT broker setup for local mesh clustering.

## File structure

- `mosquitto.conf`: Broker configuration
- `cluster_setup.md`: Deployment and topology guide

## Key settings

```
listener 1883 0.0.0.0
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
```

## Topics

All telemetry flows through hierarchical topics to support filtering and aggregation:

- `waste/bin/<id>/telemetry` — raw sensor readings
- `waste/cluster/<id>/aggregate` — cluster-level summaries
- `waste/facility/<id>/dispatch` — facility-level commands

## Bridge mode

For multi-facility deployments, configure MQTT bridge mode to relay messages between clusters without duplicating data.
