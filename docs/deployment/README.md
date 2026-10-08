# Deployment Guide

This guide provides instructions for deploying the waste-intelligence platform for prototype testing.

## Prerequisites

### Hardware Requirements
- Docker and Docker Compose installed
- Minimum 8GB RAM
- Minimum 4 CPU cores
- 50GB disk space

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+ (for local development)
- Git

## Quick Deployment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd waste-intelligence-platform
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Deploy All Services
```bash
python scripts/deploy.py deploy
```

This will:
- Check Docker installation
- Build all Docker images
- Start all services
- Initialize the database
- Seed with test data
- Verify service health

## Manual Deployment

### Build and Start Services
```bash
# Build images
docker compose -f docker-compose.yml build

# Start services
docker compose -f docker-compose.yml up -d

# Check status
docker compose -f docker-compose.yml ps
```

### Initialize Database
```bash
# Wait for PostgreSQL to start (may take 30-60 seconds)
docker compose -f docker-compose.yml exec -T postgres pg_isready -U postgres -d waste

# Run migrations
docker compose -f docker-compose.yml exec -T postgres psql -U postgres -d waste -f /docker-entrypoint-initdb.d/001_init_schema.sql

# Seed data
python scripts/seed_database.py
```

## Service Endpoints

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| MQTT Broker | `mqtt://localhost` | 1883 | IoT sensor telemetry |
| PostgreSQL | `postgresql://localhost` | 5432 | Data storage |
| Hub API | `http://localhost:5000` | 5000 | REST API for bins and facilities |
| Streamlit Dashboard | `http://localhost:8501` | 8501 | Web dashboard |
| Prometheus | `http://localhost:9090` | 9090 | Metrics collection |
| Grafana | `http://localhost:3000` | 3000 | Visualization dashboard |

## API Endpoints

### Health Check
```
GET /health
```

### Bins
```
GET /bins          - List all bins
GET /bins/{id}     - Get specific bin
POST /bins         - Create new bin
```

### Facilities
```
GET /facilities          - List all facilities
GET /facilities/{id}     - Get specific facility
POST /facilities         - Create new facility
```

### Analytics
```
GET /analytics/forecast    - Get waste forecasts
GET /analytics/routing    - Get optimal routes
```

## Health Checks

### Check All Services
```bash
python scripts/health_checks.py
```

### Check Individual Services
```bash
# Check API
curl http://localhost:5000/health

# Check database
psql -h localhost -U postgres -d waste -c "SELECT count(*) FROM bins;"

# Check MQTT
mosquitto_pub -h localhost -t "test" -m "hello" -p 1883
```

## Monitoring

### Prometheus
Access at: `http://localhost:9090`

Pre-configured to scrape:
- Hub API metrics
- Streamlit metrics
- MQTT broker metrics

### Grafana
Access at: `http://localhost:3000`

Default credentials:
- Username: `admin`
- Password: Configured in `.env` (default: `changeme`)

Pre-configured dashboards:
- Waste overview
- Bin telemetry
- Facility load

## Troubleshooting

### Common Issues

**Docker containers won't start:**
- Check Docker is running: `docker --version`
- Check port conflicts: `netstat -tuln` or `ss -tuln`
- Check logs: `docker compose -f docker-compose.yml logs`

**Database connection errors:**
- Ensure PostgreSQL is running: `docker compose -f docker-compose.yml ps`
- Check credentials in `.env` file
- Wait for database to initialize (may take 30-60 seconds)

**MQTT connection errors:**
- Check Mosquitto is running
- Verify port 1883 is open
- Check `mesh-network/mqtt/mosquitto.conf` configuration

**API not responding:**
- Check Flask is running: `docker compose -f docker-compose.yml logs hub-api`
- Verify port 5000 is open
- Check database connection from API container

### View Logs
```bash
# All services
docker compose -f docker-compose.yml logs -f

# Specific service
docker compose -f docker-compose.yml logs -f hub-api
```

### Clean Up
```bash
# Stop all containers
docker compose -f docker-compose.yml down

# Remove volumes (WARNING: This will delete all data)
docker compose -f docker-compose.yml down -v

# Remove all unused containers, networks, and images
docker system prune -a
```

## Prototype Testing

### Sensor Simulation
```bash
# Publish test telemetry
mosquitto_pub -h localhost -t "waste/bin/telemetry" -m '{"sensor_id": "test-001", "fill_level_percent": 75.5, "mass_kg": 150.0, "timestamp": "2024-01-01T12:00:00Z"}' -p 1883
```

### Test API
```bash
# Create a bin
curl -X POST http://localhost:5000/bins \
  -H "Content-Type: application/json" \
  -d '{"bin_id": "test-bin-001", "latitude": 40.7128, "longitude": -74.0060}'

# List bins
curl http://localhost:5000/bins

# Get bin
curl http://localhost:5000/bins/test-bin-001
```

### Test Forecasting
```bash
# Get forecast
curl http://localhost:5000/analytics/forecast
```

## Security Considerations

### For Production Deployment
1. Enable TLS for all services
2. Use strong passwords for all services
3. Configure firewall rules
4. Enable authentication for MQTT
5. Use HTTPS for API endpoints
6. Regularly update Docker images
7. Monitor logs for suspicious activity

### Environment Variables
Never commit `.env` files to version control. Use `.env.example` as a template.

## Performance Tuning

### Database
- Adjust `shared_buffers` in PostgreSQL configuration
- Configure `work_mem` based on available memory
- Consider partitioning large tables

### MQTT
- Adjust `max_connections` in Mosquitto configuration
- Configure `persistence` for message durability
- Set appropriate `max_inflight_messages`

### API
- Adjust Flask `workers` based on CPU cores
- Configure `timeout` settings appropriately
- Enable caching for frequently accessed endpoints

## Scaling

### Horizontal Scaling
- Run multiple instances of API containers
- Use load balancer in front of API instances
- Scale MQTT brokers for high message throughput

### Database Scaling
- Consider read replicas for analytics queries
- Use connection pooling
- Optimize queries with proper indexes

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker compose -f docker-compose.yml exec -T postgres pg_dump -U postgres waste > backup.sql

# Restore backup
cat backup.sql | docker compose -f docker-compose.yml exec -T postgres psql -U postgres waste
```

### Volume Backup
```bash
# Backup volumes
docker run --rm --volumes-from postgres -v $(pwd):/backup busybox tar cvf /backup/postgres_backup.tar /var/lib/postgresql/data

# Restore volumes
# Stop containers first, then:
docker run --rm --volumes-from postgres -v $(pwd):/backup busybox tar xvf /backup/postgres_backup.tar -C /
```
