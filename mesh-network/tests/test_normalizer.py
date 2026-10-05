"""Tests for packet normalization."""

from mesh_network.utils.packet_normalizer import normalize_payload


def test_normalize_payload():
    raw = {
        "sensor_id": "bin-001",
        "cluster_id": "cluster-01",
        "facility_id": "fac-01",
        "fill_level_percent": 50.0,
        "mass_kg": 25.0,
    }
    result = normalize_payload(raw)
    assert result["sensor_id"] == "bin-001"
    assert result["fill_level_percent"] == 50.0
    assert "timestamp" in result
