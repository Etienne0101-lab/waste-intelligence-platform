"""Forecasting utilities for facility load and diversion trends."""
from __future__ import annotations

from typing import Iterable


def linear_forecast(values: Iterable[float], horizon: int = 1) -> list[float]:
    series = list(values)
    if not series:
        return [0.0 for _ in range(horizon)]
    slope = (series[-1] - series[0]) / max(len(series) - 1, 1)
    return [series[-1] + slope * step for step in range(1, horizon + 1)]
