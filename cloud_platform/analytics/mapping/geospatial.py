"""Geospatial utilities for coordinate transforms and spatial joins."""
from __future__ import annotations

import math
from typing import Optional, Tuple


def latlon_to_tile(lat: float, lon: float, zoom: int = 13) -> Tuple[int, int, int]:
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(math.radians(lat)) + 1.0 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n)
    return (x, y, zoom)


def find_nearest_facility(bin_lat: float, bin_lon: float, facilities: list[dict]) -> Optional[dict]:
    from hub_layer.api.utils.haversine import haversine_km

    if not facilities:
        return None
    nearest = None
    min_distance = float("inf")
    for facility in facilities:
        distance = haversine_km(bin_lat, bin_lon, facility["latitude"], facility["longitude"])
        if distance < min_distance:
            nearest = facility
            min_distance = distance
    return nearest
