#!/usr/bin/env python3
"""Health check script for waste-intelligence platform services."""

from __future__ import annotations

import logging
import requests
import sys
from typing import Dict

logger = logging.getLogger(__name__)


def check_api_health() -> Dict[str, str]:
    """Check health of API endpoints."""
    results = {}
    
    # Check hub API
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        results["hub_api"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["hub_api"] = f"unreachable: {e}"
    
    # Check bins endpoint
    try:
        response = requests.get("http://localhost:5000/bins", timeout=5)
        results["bins_endpoint"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["bins_endpoint"] = f"unreachable: {e}"
    
    # Check facilities endpoint
    try:
        response = requests.get("http://localhost:5000/facilities", timeout=5)
        results["facilities_endpoint"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["facilities_endpoint"] = f"unreachable: {e}"
    
    return results


def check_database() -> Dict[str, str]:
    """Check database connectivity."""
    results = {}
    
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="waste",
            user="postgres",
            password="postgres",
            connect_timeout=5
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        results["postgres"] = "ok"
    except Exception as e:
        results["postgres"] = f"error: {e}"
    
    return results


def check_mqtt() -> Dict[str, str]:
    """Check MQTT broker connectivity."""
    results = {}
    
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect("localhost", 1883, timeout=5)
        client.disconnect()
        results["mqtt"] = "ok"
    except Exception as e:
        results["mqtt"] = f"error: {e}"
    
    return results


def check_dashboard() -> Dict[str, str]:
    """Check Streamlit dashboard."""
    results = {}
    
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        results["streamlit"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["streamlit"] = f"unreachable: {e}"
    
    return results


def check_monitoring() -> Dict[str, str]:
    """Check monitoring services."""
    results = {}
    
    # Check Prometheus
    try:
        response = requests.get("http://localhost:9090", timeout=5)
        results["prometheus"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["prometheus"] = f"unreachable: {e}"
    
    # Check Grafana
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        results["grafana"] = "ok" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        results["grafana"] = f"unreachable: {e}"
    
    return results


def run_all_checks() -> Dict[str, Dict[str, str]]:
    """Run all health checks."""
    return {
        "api": check_api_health(),
        "database": check_database(),
        "mqtt": check_mqtt(),
        "dashboard": check_dashboard(),
        "monitoring": check_monitoring(),
    }


def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    
    checks = run_all_checks()
    
    # Print results
    all_ok = True
    for category, results in checks.items():
        logger.info(f"\n{category.upper()}:")
        for service, status in results.items():
            logger.info(f"  {service}: {status}")
            if status != "ok":
                all_ok = False
    
    # Summary
    total_checks = sum(len(results) for results in checks.values())
    ok_checks = sum(1 for results in checks.values() for status in results.values() if status == "ok")
    
    logger.info(f"\nSummary: {ok_checks}/{total_checks} checks passed")
    
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
