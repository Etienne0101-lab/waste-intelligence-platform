# DevOps Configuration

This directory contains Docker, CI/CD, monitoring, and deployment configurations for the waste-intelligence platform.

## Docker Configuration

### Available Dockerfiles
- `devops/docker/api.Dockerfile` - Hub API Flask service
- `devops/docker/streamlit.Dockerfile` - Streamlit dashboard
- `devops/docker/mqtt.Dockerfile` - Eclipse Mosquitto MQTT broker
- `devops/docker/postgres.Dockerfile` - TimescaleDB PostgreSQL database
- `devops/docker/grafana.Dockerfile` - Grafana dashboard
- `devops/docker/prometheus.Dockerfile` - Prometheus monitoring

### Quick Start

1. Build all images:
   ```bash
   docker compose -f docker-compose.yml build
   ```

2. Start all services:
   ```bash
   docker compose -f docker-compose.yml up -d
   ```

3. Stop all services:
   ```bash
   docker compose -f docker-compose.yml down
   ```

## Monitoring

### Prometheus
- Configuration: `devops/monitoring/prometheus.yml`
- Scrapes metrics from all services every 15 seconds
- Access at: `http://localhost:9090`

### Grafana
- Provisioning: `cloud-platform/dashboards/grafana/provisioning/`
- Datasources, dashboards, and alerts are auto-configured
- Access at: `http://localhost:3000`
- Admin credentials: See `.env.example`

## CI/CD

### GitHub Actions
- Workflow: `devops/ci-cd/github-actions.yml`
- Runs tests on push to main/master branches
- Runs tests on pull requests to main/master

### Docker Build
- Multi-stage builds for production optimization
- Uses Python 3.11 slim base images

## Deployment

### Production Deployment
Use the deployment script:
```bash
python scripts/deploy.py deploy
```

### Service Management
```bash
# Start services
python scripts/deploy.py start

# Stop services
python scripts/deploy.py stop

# Check health
python scripts/deploy.py health
```

### Health Checks
Run comprehensive health checks:
```bash
python scripts/health_checks.py
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:
- Database credentials
- MQTT broker settings
- API host and port
- Grafana admin credentials
- Logging configuration

## Network Architecture

All services communicate via Docker's internal network:
- MQTT: Port 1883 (broker), 9001 (WebSocket)
- PostgreSQL: Port 5432
- Hub API: Port 5000
- Streamlit: Port 8501
- Prometheus: Port 9090
- Grafana: Port 3000
