"""Facility load forecasting based on current and historical mass totals."""
from __future__ import annotations

from typing import Iterable


def project_facility_load(history: Iterable[float], horizon_days: int = 7) -> float:
    values = list(history)
    if not values:
        return 0.0
    avg = sum(values) / len(values)
    return avg * float(horizon_days)
