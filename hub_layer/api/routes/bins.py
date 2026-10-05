"""Bin route handlers."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bins_bp = Blueprint("bins", __name__, url_prefix="/bins")


@bins_bp.get("")
def list_bins():
    return jsonify({"bins": [], "count": 0})


@bins_bp.get("/<bin_id>")
def get_bin(bin_id: str):
    return jsonify({"bin_id": bin_id, "status": "registered"})


@bins_bp.post("")
def create_bin():
    data = request.get_json(silent=True) or {}
    if not data.get("bin_id"):
        return jsonify({"error": "bin_id is required"}), 400
    return jsonify({"status": "created", "bin_id": data["bin_id"]}), 201
