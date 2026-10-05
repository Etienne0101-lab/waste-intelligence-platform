"""Facility data model and schema."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Facility:
    """Represents a waste treatment facility (composting, recycling, etc.)."""
    facility_id: str
    name: str
    latitude: float
    longitude: float
    facility_type: str  # e.g. "composting", "recycling", "transfer"
    capacity_kg: float
    current_load_kg: float = 0.0
    status: str = "operational"
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "facility_id": self.facility_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "facility_type": self.facility_type,
            "capacity_kg": self.capacity_kg,
            "current_load_kg": self.current_load_kg,
            "utilization_percent": round((self.current_load_kg / self.capacity_kg * 100), 2) if self.capacity_kg > 0 else 0.0,
            "status": self.status,
        }
