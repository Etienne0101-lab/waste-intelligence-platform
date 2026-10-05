# ChirpStack LoRaWAN Server

Containerized ChirpStack deployment for LoRaWAN mesh connectivity.

## Stack

- ChirpStack Application Server
- ChirpStack Network Server
- PostgreSQL backend
- Redis for caching

## Deployment

```bash
docker-compose -f devops/docker/docker-compose.yml up -d
```

## Configuration

- Region: US915 (or configure per deployment)
- Device profiles in `config/` directory
- Gateway credentials via environment variables

## API endpoints

- `/api/devices` — device management
- `/api/applications` — application management
- `/api/uplink` — uplink message handling
