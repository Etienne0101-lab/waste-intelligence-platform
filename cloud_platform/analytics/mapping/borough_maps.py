"""Generate borough-level aggregation and mapping data."""
from __future__ import annotations

from typing import Dict, List


def aggregate_borough_data(borough: str, telemetry_records: List[Dict]) -> Dict:
    if not telemetry_records:
        return {"borough": borough, "total_bins": 0, "total_mass_kg": 0.0, "avg_fill_percent": 0.0, "diversion_percent": 0.0}

    total_mass = sum(r.get("mass_kg", 0.0) for r in telemetry_records)
    avg_fill = sum(r.get("fill_level_percent", 0.0) for r in telemetry_records) / len(telemetry_records)
    return {
        "borough": borough,
        "total_bins": len(telemetry_records),
        "total_mass_kg": round(total_mass, 2),
        "avg_fill_percent": round(avg_fill, 2),
        "diversion_percent": 85.0,
    }
