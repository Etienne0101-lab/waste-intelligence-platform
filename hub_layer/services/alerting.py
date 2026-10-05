"""Operational alert generation for overflow, load, and battery warnings."""
from __future__ import annotations

from typing import Any, Dict, List


def build_alerts(metrics: Dict[str, Any]) -> List[Dict[str, str]]:
    alerts: List[Dict[str, str]] = []

    if float(metrics.get("facility_load_pct", 0.0)) > 90:
        alerts.append({"severity": "critical", "message": "Facility capacity threshold exceeded"})
    if float(metrics.get("overflow_risk", 0.0)) > 85:
        alerts.append({"severity": "warning", "message": "Bin overflow risk detected"})
    if float(metrics.get("battery_low_bins", 0.0)) > 0:
        alerts.append({"severity": "warning", "message": "Low battery bins require maintenance"})

    return alerts
