"""Facility load forecasting based on current and historical mass totals."""

from __future__ import annotations

import logging
from typing import Iterable

logger = logging.getLogger(__name__)


def project_facility_load(history: Iterable[float], horizon_days: int = 7) -> float:
    """Project upcoming facility load using a simple moving average."""
    values = list(history)
    if not values:
        return 0.0
    avg = sum(values) / len(values)
    return avg * float(horizon_days)
