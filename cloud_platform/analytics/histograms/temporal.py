"""Temporal histograms for timing-based waste analytics."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List


def build_temporal_histogram(events: Iterable[dict]) -> Dict[str, List[float]]:
    buckets: Dict[str, List[float]] = defaultdict(list)
    for event in events:
        bucket = event.get("bucket", "unknown")
        value = float(event.get("value", 0.0))
        buckets[bucket].append(value)
    return dict(buckets)
