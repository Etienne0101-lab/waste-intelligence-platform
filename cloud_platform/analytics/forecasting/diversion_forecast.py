"""Diversion performance forecasting using historical trends."""
from __future__ import annotations

from typing import Iterable, Optional


def forecast_diversion_rate(historical_diversion: Iterable[float], periods_ahead: int = 7) -> Optional[float]:
    rates = list(historical_diversion)
    if not rates:
        return None
    avg_rate = sum(rates) / len(rates)
    trend = (rates[-1] - rates[0]) / max(len(rates) - 1, 1) if len(rates) > 1 else 0
    forecast = avg_rate + trend * periods_ahead
    return max(0.0, min(100.0, forecast))
