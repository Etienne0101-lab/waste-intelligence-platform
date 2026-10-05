"""Application bootstrap script for infrastructure setup and validation."""
from __future__ import annotations

from scripts.seed_data import BIN_SEED, FACILITY_SEED
from scripts.validate_stack import run_smoke_checks, run_python_import_validation


def bootstrap() -> dict:
    validation = run_smoke_checks()
    imports = run_python_import_validation()
    return {
        "stack_layout": validation,
        "imports": imports,
        "seed_bins": len(BIN_SEED),
        "seed_facilities": len(FACILITY_SEED),
    }


if __name__ == "__main__":
    print(bootstrap())
