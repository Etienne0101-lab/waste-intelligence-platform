"""Inference engine for real-time and batch ML predictions."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch

from .anomaly_detection import ClusterAnomalyDetector
from .model_registry import ModelRegistry

LOGGER = logging.getLogger(__name__)


class MLInferenceEngine:
    """High-level inference interface for ingestion services and batch jobs."""

    def __init__(self, model_registry_path: str | Path | None = None) -> None:
        self.registry = ModelRegistry(registry_path=model_registry_path)

    def predict_contamination(
        self,
        sensor_metadata: dict[str, float] | None = None,
        image: Any | None = None,
        image_path: str | None = None,
        gas_signal: list[float] | np.ndarray | None = None,
        model_name: str = "contamination_cnn",
        version: str | None = None,
    ) -> dict[str, Any]:
        """Run contamination classification inference using a stored CNN model."""
        model = self.registry.load_model(model_name=model_name, version=version)
        if not isinstance(model, torch.nn.Module):
            raise TypeError("The contamination model must be a PyTorch module for inference.")

        model.eval()
        sensor_vector = self._prepare_sensor_vector(sensor_metadata)
        gas_vector = np.asarray(gas_signal, dtype=np.float32).reshape(-1) if gas_signal is not None else None

        image_tensor = None
        if image is not None:
            if isinstance(image, str):
                image_tensor = self._load_image_tensor(image)
            else:
                image_tensor = torch.as_tensor(np.asarray(image, dtype=np.float32) / 255.0)
                if image_tensor.dim() == 3:
                    image_tensor = image_tensor.permute(2, 0, 1)
                if image_tensor.dim() == 2:
                    image_tensor = image_tensor.unsqueeze(0)
        elif image_path:
            image_tensor = self._load_image_tensor(image_path)

        with torch.no_grad():
            metadata_vector = sensor_vector
            logits = model(
                image=image_tensor,
                sensor=torch.tensor(sensor_vector, dtype=torch.float32),
                gas_signal=torch.tensor(gas_vector, dtype=np.float32) if gas_vector is not None else None,
                metadata=torch.tensor(metadata_vector, dtype=np.float32),
            )
            probabilities = torch.softmax(logits, dim=1)
            prediction_idx = int(torch.argmax(probabilities, dim=1).item())
            confidence = float(probabilities[0, prediction_idx].item())

        return {
            "model_name": model_name,
            "version": version,
            "prediction": prediction_idx,
            "confidence": confidence,
            "probabilities": probabilities[0].cpu().numpy().tolist(),
        }

    def forecast_waste(
        self,
        features: pd.DataFrame,
        model_name: str = "waste_forecast",
        version: str | None = None,
    ) -> np.ndarray:
        """Forecast waste output using a trained regression model."""
        model = self.registry.load_model(model_name=model_name, version=version)
        return np.asarray(model.predict(features), dtype=float)

    def predict_facility_load(
        self,
        features: pd.DataFrame,
        model_name: str = "facility_load",
        version: str | None = None,
    ) -> np.ndarray:
        """Predict facility congestion or load."""
        model = self.registry.load_model(model_name=model_name, version=version)
        return np.asarray(model.predict(features), dtype=float)

    def detect_cluster_anomalies(
        self,
        features: pd.DataFrame,
        feature_columns: list[str],
        model_name: str = "cluster_anomaly",
        version: str | None = None,
    ) -> pd.DataFrame:
        """Apply cluster anomaly detection to input feature rows."""
        model = self.registry.load_model(model_name=model_name, version=version)
        if not isinstance(model, ClusterAnomalyDetector):
            raise TypeError("The anomaly model must be a ClusterAnomalyDetector instance.")
        labels = model.predict(features[feature_columns])
        scores = model.score_samples(features[feature_columns])
        result = features.copy()
        result["anomaly_label"] = labels
        result["anomaly_score"] = scores
        result["is_anomaly"] = result["anomaly_label"] == -1
        return result

    @staticmethod
    def _prepare_sensor_vector(sensor_metadata: dict[str, float] | None) -> np.ndarray:
        if sensor_metadata is None:
            return np.zeros(8, dtype=np.float32)

        values = [float(v) for _, v in sorted(sensor_metadata.items())]
        if not values:
            return np.zeros(8, dtype=np.float32)

        vector = np.asarray(values, dtype=np.float32)
        if vector.size < 8:
            vector = np.pad(vector, (0, 8 - vector.size), mode="constant")
        return vector[:8]

    @staticmethod
    def _load_image_tensor(image_path: str) -> torch.Tensor:
        from PIL import Image

        with Image.open(image_path) as img:
            img = img.convert("RGB")
            arr = np.asarray(img, dtype=np.float32) / 255.0
            arr = np.transpose(arr, (2, 0, 1))
            return torch.from_numpy(arr).unsqueeze(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Inference engine module loaded.")
