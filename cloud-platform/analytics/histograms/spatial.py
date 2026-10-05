"""Spatial histograms for building, block, and borough aggregations."""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, Iterable, List

logger = logging.getLogger(__name__)


def build_spatial_histogram(
    events: Iterable[Dict[str, any]], level: str = "building"
) -> Dict[str, List[float]]:
    """Aggregate values by geographic level (building, block, neighborhood, borough)."""
    buckets: Dict[str, List[float]] = defaultdict(list)

    for event in events:
        if level == "building":
            bucket_key = event.get("building_id", "unknown")
        elif level == "block":
            bucket_key = event.get("block_id", "unknown")
        elif level == "neighborhood":
            bucket_key = event.get("neighborhood", "unknown")
        elif level == "borough":
            bucket_key = event.get("borough", "unknown")
        else:
            bucket_key = "unknown"

        value = float(event.get("mass_kg", 0.0))
        buckets[bucket_key].append(value)

    return dict(buckets)
