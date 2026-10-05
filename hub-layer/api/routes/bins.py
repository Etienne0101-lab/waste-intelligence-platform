"""Bin route handlers."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

bins_bp = Blueprint("bins", __name__, url_prefix="/bins")


@bins_bp.get("")
def list_bins():
    """Return available bin metadata."""
    return jsonify({"bins": [], "count": 0})


@bins_bp.get("/<bin_id>")
def get_bin(bin_id: str):
    """Return a specific bin by ID."""
    return jsonify({"bin_id": bin_id, "status": "registered"})


@bins_bp.post("")
def create_bin():
    """Register a new bin."""
    data = request.get_json(silent=True) or {}
    if not data.get("bin_id"):
        return jsonify({"error": "bin_id is required"}), 400
    return jsonify({"status": "created", "bin_id": data["bin_id"]}), 201
