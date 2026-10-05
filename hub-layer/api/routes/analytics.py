"""Analytics endpoint for hub-level operational insights."""

from __future__ import annotations

from flask import Blueprint, jsonify

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.get("/summary")
def summary():
    """Return a simple aggregate summary for regional analysis."""
    return jsonify({
        "total_bins": 0,
        "total_facilities": 0,
        "average_fill_percent": 0.0,
        "forecast_status": "pending".
    })
