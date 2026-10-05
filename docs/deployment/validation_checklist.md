# Deployment validation checklist

- Run `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and populate secrets
- Start services with `docker-compose up -d`
- Run `python scripts/run_smoke_checks.py`
- Open `http://localhost:5000/health`
- Open `http://localhost:8501`
- Confirm Prometheus is scraping metrics and Grafana can read the datasource
- Validate that MQTT, database, API, and dashboard services are all reachable
