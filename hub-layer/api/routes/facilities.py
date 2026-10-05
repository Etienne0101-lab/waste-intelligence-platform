"""Facility route handlers."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

facilities_bp = Blueprint("facilities", __name__, url_prefix="/facilities")


@facilities_bp.get("")
def list_facilities():
    """Return all facility metadata."""
    return jsonify({"facilities": [], "count": 0})


@facilities_bp.post("")
def create_facility():
    """Register a new facility."""
    data = request.get_json(silent=True) or {}
    if not data.get("facility_id"):
        return jsonify({"error": "facility_id is required"}), 400
    return jsonify({"status": "created", "facility_id": data["facility_id"]}), 201
