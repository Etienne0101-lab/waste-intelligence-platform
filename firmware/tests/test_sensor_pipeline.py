"""Example test coverage for module smoke checks."""

from hub_layer.api.utils.haversine import haversine_km


def test_haversine_distance():
    assert haversine_km(40.7128, -74.0060, 40.7306, -73.9352) > 0
