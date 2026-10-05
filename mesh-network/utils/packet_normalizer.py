"""Utilities for packet normalization before upstream transmission."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger(__name__)


def normalize_payload(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw telemetry to a canonical data structure."""
    try:
        normalized = {
            "sensor_id": raw_payload.get("sensor_id", "unknown"),
            "cluster_id": raw_payload.get("cluster_id", "unknown"),
            "facility_id": raw_payload.get("facility_id", "unknown"),
            "fill_level_percent": float(raw_payload.get("fill_level_percent", 0.0)),
            "mass_kg": float(raw_payload.get("mass_kg", 0.0)),
            "timestamp": raw_payload.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }
        return normalized
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to normalize payload: %s", exc)
        raise
