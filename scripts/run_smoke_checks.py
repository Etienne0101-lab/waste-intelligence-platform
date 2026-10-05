"""Startup validation and deployment smoke checks."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_smoke_checks() -> dict:
    root = Path(__file__).resolve().parent.parent
    checks = {
        "requirements_exists": (root / "requirements.txt").exists(),
        "docker_compose_exists": (root / "docker-compose.yml").exists(),
        "env_example_exists": (root / ".env.example").exists(),
        "hub_api_exists": (root / "hub_layer" / "api" / "app.py").exists(),
        "dashboard_exists": (root / "cloud_platform" / "dashboards" / "streamlit" / "app.py").exists(),
    }
    return checks


def run_python_import_validation() -> dict:
    imports = [
        "hub_layer.api.app",
        "hub_layer.services.facility_routing",
        "mesh_network.utils.packet_normalizer",
        "cloud_platform.ingestion.mqtt_ingest",
        "cloud_platform.analytics.forecasting.regression",
    ]
    results = {}
    for module in imports:
        try:
            __import__(module)
            results[module] = "ok"
        except Exception as exc:  # pragma: no cover
            results[module] = str(exc)
    return results


if __name__ == "__main__":
    print(run_smoke_checks())
    print(run_python_import_validation())
