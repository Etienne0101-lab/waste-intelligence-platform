"""Analytics service for throughput forecasting and load forecasting."""
from __future__ import annotations

from typing import Iterable, List

from cloud_platform.analytics.forecasting.regression import forecast_with_linear_regression


def generate_throughput_forecast(history: Iterable[float], horizon_steps: int = 7) -> List[float]:
    return forecast_with_linear_regression(history, horizon_steps=horizon_steps)


def estimate_route_efficiency(route_distances: Iterable[float]) -> float:
    distances = list(route_distances)
    if not distances:
        return 0.0
    return round(sum(distances) / len(distances), 2)
