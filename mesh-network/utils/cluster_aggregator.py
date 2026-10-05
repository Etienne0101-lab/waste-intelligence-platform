"""Cluster aggregation service for local mesh nodes."""

from __future__ import annotations

import logging
from statistics import mean
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def aggregate_cluster(readings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate multiple bin readings into a single cluster payload."""
    if not readings:
        raise ValueError("No readings available for aggregation")

    try:
        cluster_payload = {
            "cluster_id": readings[0].get("cluster_id", "unknown"),
            "facility_id": readings[0].get("facility_id", "unknown"),
            "bin_count": len(readings),
            "avg_fill_level_percent": round(mean(item.get("fill_level_percent", 0.0) for item in readings), 2),
            "total_mass_kg": round(sum(item.get("mass_kg", 0.0) for item in readings), 2),
            "peak_fill_percent": max(item.get("fill_level_percent", 0.0) for item in readings),
        }
        return cluster_payload
    except Exception as exc:  # pragma: no cover
        logger.exception("Cluster aggregation failed: %s", exc)
        raise
