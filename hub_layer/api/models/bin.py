"""Bin data model."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Bin:
    bin_id: str
    cluster_id: str
    facility_id: str
    latitude: float
    longitude: float
    fill_level_percent: float = 0.0
    mass_kg: float = 0.0
    status: str = "active"
    last_reading: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    battery_percent: int = 100
    contaminated: bool = False

    def to_dict(self) -> dict:
        return {
            "bin_id": self.bin_id,
            "cluster_id": self.cluster_id,
            "facility_id": self.facility_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "fill_level_percent": self.fill_level_percent,
            "mass_kg": self.mass_kg,
            "status": self.status,
            "battery_percent": self.battery_percent,
            "contaminated": self.contaminated,
        }
