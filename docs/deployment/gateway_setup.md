# Gateway Setup

## Objectives

Gateways provide resilient uplink to the wider platform and aggregate local data from clusters.

## Deployment checklist

- Confirm LoRaWAN or MQTT connectivity
- Configure cluster metadata and device mapping
- Validate broker reachability
- Validate secure credentials via environment variables
- Confirm time synchronization across devices

## Monitoring

Use Prometheus and Grafana dashboards to verify uptime, message rates, packet loss, and gateway health.
