#!/usr/bin/env python3
"""Deployment orchestration script for waste-intelligence platform."""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


def run_command(cmd: List[str], cwd: Optional[str] = None) -> bool:
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"stdout: {result.stdout}")
            logger.error(f"stderr: {result.stderr}")
            return False
        logger.info(f"Command succeeded: {' '.join(cmd)}")
        return True
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(cmd)}")
        return False
    except Exception as e:
        logger.error(f"Command error: {e}")
        return False


def check_docker_installed() -> bool:
    """Check if Docker is installed and running."""
    return run_command(["docker", "--version"])


def check_docker_compose_installed() -> bool:
    """Check if Docker Compose is installed."""
    return run_command(["docker", "compose", "version"])


def build_images() -> bool:
    """Build all Docker images."""
    logger.info("Building Docker images...")
    
    images = [
        "api",
        "streamlit",
        "mqtt",
        "grafana",
        "prometheus",
        "postgres",
    ]
    
    for image in images:
        dockerfile = f"devops/docker/{image}.Dockerfile"
        if not Path(dockerfile).exists():
            logger.warning(f"Dockerfile not found: {dockerfile}")
            continue
        
        if not run_command([
            "docker", "build",
            "-t", f"waste-intelligence-{image}",
            "-f", dockerfile,
            "."
        ]):
            return False
    
    return True


def start_services() -> bool:
    """Start all services using Docker Compose."""
    logger.info("Starting services with Docker Compose...")
    
    return run_command([
        "docker", "compose",
        "-f", "docker-compose.yml",
        "up", "-d"
    ])


def stop_services() -> bool:
    """Stop all services."""
    logger.info("Stopping services...")
    
    return run_command([
        "docker", "compose",
        "-f", "docker-compose.yml",
        "down"
    ])


def check_service_health() -> dict:
    """Check health of all services."""
    services = {
        "mqtt": "1883",
        "postgres": "5432",
        "hub-api": "5000",
        "streamlit": "8501",
        "prometheus": "9090",
    }
    
    results = {}
    for service, port in services.items():
        # Simple check - in production, use proper health endpoints
        results[service] = "unknown"
    
    return results


def initialize_database() -> bool:
    """Initialize the database schema."""
    logger.info("Initializing database...")
    
    # Wait for PostgreSQL to be ready
    if not run_command([
        "docker", "compose",
        "-f", "docker-compose.yml",
        "exec", "-T", "postgres",
        "pg_isready", "-U", "postgres", "-d", "waste",
        "--timeout=30"
    ]):
        logger.warning("PostgreSQL not ready yet")
        return False
    
    # Run migrations
    return run_command([
        "docker", "compose",
        "-f", "docker-compose.yml",
        "exec", "-T", "postgres",
        "psql", "-U", "postgres", "-d", "waste",
        "-f", "/docker-entrypoint-initdb.d/001_init_schema.sql"
    ])


def seed_data() -> bool:
    """Seed the database with initial data."""
    logger.info("Seeding database...")
    
    # Use psycopg2 to insert seed data
    seed_script = """
import psycopg2
from scripts.seed_data import BIN_SEED, FACILITY_SEED

conn = psycopg2.connect(
    host="postgres",
    database="waste",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

for bin_data in BIN_SEED:
    cur.execute(
        "INSERT INTO bins (bin_id, cluster_id, facility_id, latitude, longitude, status) "
        "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (bin_id) DO NOTHING",
        (bin_data["bin_id"], bin_data.get("cluster_id"), bin_data.get("facility_id"),
         bin_data["latitude"], bin_data["longitude"], bin_data.get("status", "active"))
    )

for facility in FACILITY_SEED:
    cur.execute(
        "INSERT INTO facilities (facility_id, name, facility_type, latitude, longitude, capacity_kg) "
        "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (facility_id) DO NOTHING",
        (facility["facility_id"], facility["name"], facility.get("facility_type", "unknown"),
         facility["latitude"], facility["longitude"], facility["capacity_kg"])
    )

conn.commit()
cur.close()
conn.close()
"""
    
    # Write seed script to temp file
    seed_file = Path("/tmp/seed_database.py")
    seed_file.write_text(seed_script)
    
    # Run seed script in hub-api container
    return run_command([
        "docker", "compose",
        "-f", "docker-compose.yml",
        "exec", "-T", "hub-api",
        "python", str(seed_file)
    ])


def deploy() -> dict:
    """Full deployment workflow."""
    results = {"success": False, "steps": {}}
    
    # Check prerequisites
    if not check_docker_installed():
        results["steps"]["docker_check"] = "failed"
        return results
    
    results["steps"]["docker_check"] = "passed"
    
    if not check_docker_compose_installed():
        results["steps"]["docker_compose_check"] = "failed"
        return results
    
    results["steps"]["docker_compose_check"] = "passed"
    
    # Stop existing services
    stop_services()
    results["steps"]["stop_services"] = "completed"
    
    # Build images
    if not build_images():
        results["steps"]["build_images"] = "failed"
        return results
    
    results["steps"]["build_images"] = "completed"
    
    # Start services
    if not start_services():
        results["steps"]["start_services"] = "failed"
        return results
    
    results["steps"]["start_services"] = "completed"
    
    # Initialize database
    if not initialize_database():
        results["steps"]["initialize_database"] = "failed"
        return results
    
    results["steps"]["initialize_database"] = "completed"
    
    # Seed data
    if not seed_data():
        results["steps"]["seed_data"] = "failed"
        return results
    
    results["steps"]["seed_data"] = "completed"
    
    # Check service health
    results["steps"]["service_health"] = check_service_health()
    
    results["success"] = True
    return results


def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    
    action = sys.argv[1] if len(sys.argv) > 1 else "deploy"
    
    if action == "deploy":
        result = deploy()
        logger.info(f"Deployment result: {result}")
        sys.exit(0 if result["success"] else 1)
    elif action == "start":
        if start_services():
            logger.info("Services started successfully")
            sys.exit(0)
        else:
            logger.error("Failed to start services")
            sys.exit(1)
    elif action == "stop":
        if stop_services():
            logger.info("Services stopped successfully")
            sys.exit(0)
        else:
            logger.error("Failed to stop services")
            sys.exit(1)
    elif action == "health":
        health = check_service_health()
        logger.info(f"Service health: {health}")
        sys.exit(0)
    else:
        logger.error(f"Unknown action: {action}")
        logger.error("Usage: python deploy.py [deploy|start|stop|health]")
        sys.exit(1)


if __name__ == "__main__":
    main()
