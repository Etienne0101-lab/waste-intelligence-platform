"""This module contains runtime configuration and deployment metadata."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class RuntimeConfig:
    host: str = os.getenv("HUB_HOST", "0.0.0.0")
    port: int = int(os.getenv("HUB_PORT", "5000"))
    log_level: str = os.getenv("HUB_LOG_LEVEL", "INFO")
    app_secret_key: str = os.getenv("APP_SECRET_KEY", "local-dev-secret")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/waste")
    mqtt_broker_host: str = os.getenv("MQTT_BROKER_HOST", "mqtt")
    mqtt_broker_port: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    grafana_admin_password: str = os.getenv("GRAFANA_ADMIN_PASSWORD", "changeme")


DEFAULT_RUNTIME_CONFIG = RuntimeConfig()
