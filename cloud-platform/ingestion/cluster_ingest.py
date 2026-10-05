"""Cluster-level aggregate ingestion from mesh gateways."""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def ingest_cluster_aggregate(aggregate_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and store a cluster-level aggregate payload."""
    try:
        required = {"cluster_id", "bin_count", "total_mass_kg"}
        missing = required - aggregate_payload.keys()
        if missing:
            raise ValueError(f"Missing fields: {missing}")

        cleaned = {
            "cluster_id": aggregate_payload["cluster_id"],
            "facility_id": aggregate_payload.get("facility_id", "unknown"),
            "bin_count": int(aggregate_payload["bin_count"]),
            "total_mass_kg": float(aggregate_payload["total_mass_kg"]),
            "avg_fill_level": float(aggregate_payload.get("avg_fill_level_percent", 0.0)),
            "peak_fill_level": float(aggregate_payload.get("peak_fill_percent", 0.0)),
        }
        logger.info(f"Cluster aggregate accepted: {cleaned['cluster_id']}")
        return cleaned
    except Exception as exc:  # pragma: no cover
        logger.exception(f"Cluster aggregate rejected: {exc}")
        raise
