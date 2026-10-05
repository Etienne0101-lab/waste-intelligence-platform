"""Tests for ingestion services."""

import pytest
from cloud_platform.ingestion.mqtt_ingest import ingest_mqtt_payload


def test_mqtt_payload_valid():
    payload = {
        "sensor_id": "bin-001",
        "fill_level_percent": 45.0,
        "mass_kg": 18.5,
        "timestamp": "2026-10-05T00:00:00Z",
    }
    result = ingest_mqtt_payload(payload)
    assert result["sensor_id"] == "bin-001"
    assert result["mass_kg"] == 18.5


def test_mqtt_payload_missing_fields():
    payload = {"sensor_id": "bin-001"}
    with pytest.raises(ValueError):
        ingest_mqtt_payload(payload)
