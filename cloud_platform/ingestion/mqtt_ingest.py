"""Ingestion service for MQTT-based telemetry."""
from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def ingest_mqtt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = {"sensor_id", "fill_level_percent", "mass_kg"}
    missing = required_fields - payload.keys()
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    cleaned = {
        "sensor_id": payload["sensor_id"],
        "fill_level_percent": float(payload["fill_level_percent"]),
        "mass_kg": float(payload["mass_kg"]),
        "timestamp": payload.get("timestamp"),
    }
    logger.info("Accepted telemetry for sensor %s", cleaned["sensor_id"])
    return cleaned
