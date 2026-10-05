"""Spatial histograms for building, block, and borough aggregations."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List


def build_spatial_histogram(events: Iterable[dict], level: str = "building") -> Dict[str, List[float]]:
    buckets: Dict[str, List[float]] = defaultdict(list)
    for event in events:
        if level == "building":
            key = event.get("building_id", "unknown")
        elif level == "block":
            key = event.get("block_id", "unknown")
        elif level == "neighborhood":
            key = event.get("neighborhood", "unknown")
        elif level == "borough":
            key = event.get("borough", "unknown")
        else:
            key = "unknown"
        buckets[key].append(float(event.get("mass_kg", 0.0)))
    return dict(buckets)
