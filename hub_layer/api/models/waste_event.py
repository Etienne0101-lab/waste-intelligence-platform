"""Waste event model."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class WasteType(str, Enum):
    ORGANIC = "organic"
    RECYCLING = "recycling"
    LANDFILL = "landfill"
    CONTAMINATED = "contaminated"


@dataclass
class WasteEvent:
    event_id: str
    bin_id: str
    cluster_id: str
    facility_id: str
    waste_type: WasteType
    mass_kg: float
    timestamp: datetime | None = None
    notes: str = ""

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "bin_id": self.bin_id,
            "cluster_id": self.cluster_id,
            "facility_id": self.facility_id,
            "waste_type": self.waste_type.value,
            "mass_kg": self.mass_kg,
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes,
        }
