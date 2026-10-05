"""Example seed data for facilities, bins, and route planning."""
from __future__ import annotations

BIN_SEED = [
    {"bin_id": "bin-001", "latitude": 40.7128, "longitude": -74.0060, "cluster_id": "cluster-01", "facility_id": "facility-01", "status": "active"},
    {"bin_id": "bin-002", "latitude": 40.7200, "longitude": -73.9900, "cluster_id": "cluster-01", "facility_id": "facility-01", "status": "active"},
    {"bin_id": "bin-003", "latitude": 40.7500, "longitude": -73.9950, "cluster_id": "cluster-02", "facility_id": "facility-02", "status": "active"},
]

FACILITY_SEED = [
    {"facility_id": "facility-01", "name": "North Composting Hub", "facility_type": "composting", "latitude": 40.7282, "longitude": -73.9942, "capacity_kg": 5000.0, "current_load_kg": 2600.0},
    {"facility_id": "facility-02", "name": "East Recycling Hub", "facility_type": "recycling", "latitude": 40.7420, "longitude": -73.9810, "capacity_kg": 4000.0, "current_load_kg": 1800.0},
]
