"""Tests for mesh cluster aggregator."""

from mesh_network.utils.cluster_aggregator import aggregate_cluster


def test_aggregate_cluster():
    readings = [
        {"cluster_id": "cluster-01", "facility_id": "fac-01", "fill_level_percent": 40.0, "mass_kg": 20.0},
        {"cluster_id": "cluster-01", "facility_id": "fac-01", "fill_level_percent": 60.0, "mass_kg": 30.0},
    ]
    result = aggregate_cluster(readings)
    assert result["bin_count"] == 2
    assert result["total_mass_kg"] == 50.0
    assert result["avg_fill_level_percent"] == 50.0
