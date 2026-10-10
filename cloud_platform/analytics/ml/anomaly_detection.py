"""Anomaly detection for cluster-level operational drift and outlier detection."""

from __future__ import annotations

import logging
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)


class ClusterAnomalyDetector:
    """Isolation Forest-based anomaly detector for cluster-level time series and telemetry data."""

    def __init__(self, contamination: float = 0.05, random_state: int | None = None) -> None:
        self.contamination = contamination
        self.random_state = int(random_state or int(os.getenv("MODEL_SEED", "42")))
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=200,
        )

    def fit(self, features: pd.DataFrame | np.ndarray) -> "ClusterAnomalyDetector":
        data = self._coerce_to_numpy(features)
        if data.size == 0:
            raise ValueError("Feature matrix is empty.")
        scaled = self.scaler.fit_transform(data)
        self.model.fit(scaled)
        return self

    def predict(self, features: pd.DataFrame | np.ndarray) -> np.ndarray:
        if not hasattr(self.model, "n_estimators"):
            raise RuntimeError("The detector must be fit before calling predict().")
        data = self._coerce_to_numpy(features)
        scaled = self.scaler.transform(data)
        labels = self.model.predict(scaled)
        return labels

    def score_samples(self, features: pd.DataFrame | np.ndarray) -> np.ndarray:
        if not hasattr(self.model, "n_estimators"):
            raise RuntimeError("The detector must be fit before calling score_samples().")
        data = self._coerce_to_numpy(features)
        scaled = self.scaler.transform(data)
        return self.model.score_samples(scaled)

    @staticmethod
    def _coerce_to_numpy(features: pd.DataFrame | np.ndarray) -> np.ndarray:
        if isinstance(features, pd.DataFrame):
            return features.to_numpy(dtype=float)
        arr = np.asarray(features, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        return arr


def detect_anomalies(
    data: pd.DataFrame,
    feature_columns: list[str],
    contamination: float = 0.05,
    random_state: int | None = None,
) -> pd.DataFrame:
    """Fit a detector and return a dataframe annotated with anomaly labels and scores."""
    if not feature_columns:
        raise ValueError("At least one feature column must be provided.")

    missing = [col for col in feature_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    detector = ClusterAnomalyDetector(contamination=contamination, random_state=random_state)
    X = data[feature_columns]
    detector.fit(X)
    labels = detector.predict(X)
    scores = detector.score_samples(X)

    result = data.copy()
    result["anomaly_label"] = labels
    result["anomaly_score"] = scores
    result["is_anomaly"] = result["anomaly_label"] == -1
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Cluster anomaly detector module loaded successfully.")
