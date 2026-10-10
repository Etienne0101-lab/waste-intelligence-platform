"""Registry and version management for the waste-intelligence ML layer."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import torch

LOGGER = logging.getLogger(__name__)


class ModelRegistry:
    """Persist model metadata and artifacts in a versioned registry."""

    def __init__(
        self,
        base_path: str | Path | None = None,
        registry_path: str | Path | None = None,
    ) -> None:
        self.base_path = Path(base_path or os.getenv("MODEL_STORAGE_PATH", "/models"))
        self.registry_path = Path(
            registry_path or os.getenv("MODEL_REGISTRY_PATH", str(self.base_path / "model_registry.json"))
        )
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_registry()

    def _ensure_registry(self) -> None:
        if not self.registry_path.exists():
            self.registry_path.write_text(json.dumps({}, indent=2), encoding="utf-8")

    def _read_registry(self) -> dict[str, Any]:
        try:
            with self.registry_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            return payload if isinstance(payload, dict) else {}
        except json.JSONDecodeError:
            LOGGER.warning("Registry file was unreadable; resetting the registry.")
            self.registry_path.write_text(json.dumps({}, indent=2), encoding="utf-8")
            return {}

    def _write_registry(self, payload: dict[str, Any]) -> None:
        with self.registry_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)

    @staticmethod
    def _utc_timestamp() -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def _model_directory(self, model_name: str) -> Path:
        directory = self.base_path / model_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def register_model(
        self,
        model_name: str,
        model_type: str,
        artifact_path: str | Path,
        metrics: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Register a serialized model artifact and metadata for retrieval."""
        if not model_name:
            raise ValueError("model_name must not be empty.")

        artifact = Path(artifact_path)
        if not artifact.is_absolute():
            artifact = self.base_path / artifact

        if not artifact.exists():
            raise FileNotFoundError(f"Artifact does not exist: {artifact}")

        resolved_version = version or self._utc_timestamp()
        record = {
            "model_name": model_name,
            "model_type": model_type,
            "version": resolved_version,
            "artifact_path": str(artifact),
            "metrics": metrics or {},
            "metadata": metadata or {},
            "registered_at": self._utc_timestamp(),
        }

        registry = self._read_registry()
        registry.setdefault(model_name, {})
        registry[model_name][resolved_version] = record
        self._write_registry(registry)
        LOGGER.info("Registered model '%s' version '%s' at %s", model_name, resolved_version, artifact)
        return record

    def list_models(self) -> dict[str, dict[str, Any]]:
        return self._read_registry()

    def get_latest(self, model_name: str) -> dict[str, Any] | None:
        registry = self._read_registry()
        versions = registry.get(model_name, {})
        if not versions:
            return None
        latest_version = max(versions.keys(), key=lambda key: key)
        return versions[latest_version]

    def load_model(self, model_name: str, version: str | None = None) -> Any:
        """Load a model by name and optional version."""
        registry = self._read_registry()
        versions = registry.get(model_name)
        if not versions:
            raise KeyError(f"No model named '{model_name}' was found in the registry.")

        target_version = version or max(versions.keys(), key=lambda key: key)
        record = versions.get(target_version)
        if not record:
            raise KeyError(f"The version '{version}' for model '{model_name}' does not exist.")

        artifact = Path(record["artifact_path"])
        if not artifact.exists():
            raise FileNotFoundError(f"Model artifact not found for '{model_name}': {artifact}")

        model_type = str(record.get("model_type", "")).lower()
        if "torch" in model_type or artifact.suffix == ".pt":
            return torch.load(artifact, map_location="cpu")
        if "sklearn" in model_type or artifact.suffix in {".joblib", ".pkl", ".pickle"}:
            return joblib.load(artifact)
        return artifact

    def load_latest(self, model_name: str) -> Any:
        return self.load_model(model_name=model_name, version=None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Model registry started.")
