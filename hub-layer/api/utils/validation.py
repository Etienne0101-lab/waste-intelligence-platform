"""Input validation and schema checking."""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def validate_telemetry_payload(payload: Dict[str, Any]) -> tuple[bool, str]:
    """Validate incoming telemetry payload schema."""
    required_fields = {"sensor_id", "fill_level_percent", "mass_kg"}
    missing = required_fields - payload.keys()

    if missing:
        return False, f"Missing required fields: {sorted(missing)}"

    try:
        fill = float(payload["fill_level_percent"])
        mass = float(payload["mass_kg"])

        if not (0 <= fill <= 100):
            return False, "fill_level_percent must be between 0 and 100"

        if mass < 0:
            return False, "mass_kg must be non-negative"

        return True, ""
    except (ValueError, TypeError) as e:
        return False, f"Invalid field types: {e}"
