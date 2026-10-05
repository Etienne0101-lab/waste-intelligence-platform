"""Temporal histograms for timing-based waste analytics."""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, Iterable, List

logger = logging.getLogger(__name__)


def build_temporal_histogram(events: Iterable[Dict[str, float]]) -> Dict[str, List[float]]:
    """Aggregate values by time bucket for hourly or daily summaries."""
    buckets: Dict[str, List[float]] = defaultdict(list)
    for event in events:
        bucket = event.get("bucket", "unknown")
        value = float(event.get("value", 0.0))
        buckets[bucket].append(value)

    return {key: values for key, values in buckets.items()}
