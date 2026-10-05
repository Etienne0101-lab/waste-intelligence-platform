"""Service health checks for the full stack."""
from __future__ import annotations

import requests


def check_hub_api(url: str = "http://localhost:5000/health") -> dict:
    try:
        response = requests.get(url, timeout=5)
        return {"status_code": response.status_code, "body": response.json()}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "detail": str(exc)}


def check_streamlit(url: str = "http://localhost:8501") -> dict:
    try:
        response = requests.get(url, timeout=5)
        return {"status_code": response.status_code, "body": response.text[:200]}
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "detail": str(exc)}
