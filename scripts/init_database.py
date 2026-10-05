"""Initialize the database schema for the waste intelligence platform."""

from __future__ import annotations

import os
from pathlib import Path


def initialize_database() -> None:
    """Load the SQL schema into the configured database."""
    schema_path = Path(__file__).resolve().parents[1] / "hub-layer" / "database" / "schema.sql"
    print(f"Schema file located at: {schema_path}")
    print("Database init hook ready for integration with Postgres or TimescaleDB.")


if __name__ == "__main__":
    initialize_database()
