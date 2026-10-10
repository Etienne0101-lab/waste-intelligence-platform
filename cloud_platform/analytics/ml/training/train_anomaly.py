"""Train and save cluster anomaly detection models."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import joblib
import pandas as pd

from ..anomaly_detection import ClusterAnomalyDetector, detect_anomalies
from ..model_registry import ModelRegistry

LOGGER = logging.getLogger(__name__)


def train_anomaly_model(
    input_csv: str | Path,
    feature_columns: list[str],
    output_dir: str | Path | None = None,
    contamination: float = 0.05,
    random_state: int = 42,
) -> dict[str, float | str]:
    """Train an anomaly model and register it in the model registry."""
    df = pd.read_csv(input_csv)
    if df.empty:
        raise ValueError("Input CSV is empty.")

    missing = [col for col in feature_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing anomaly feature columns: {missing}")

    detector = ClusterAnomalyDetector(contamination=contamination, random_state=random_state)
    detector.fit(df[feature_columns])
    annotated = detect_anomalies(df, feature_columns=feature_columns, contamination=contamination, random_state=random_state)
    anomaly_rate = float(annotated["is_anomaly"].mean())

    output_root = Path(output_dir or os.getenv("MODEL_STORAGE_PATH", "/models")) / "cluster_anomaly"
    output_root.mkdir(parents=True, exist_ok=True)
    artifact_path = output_root / "cluster_anomaly.joblib"
    joblib.dump(detector, artifact_path)

    registry = ModelRegistry()
    registry.register_model(
        model_name="cluster_anomaly",
        model_type="sklearn",
        artifact_path=artifact_path,
        metrics={"anomaly_rate": anomaly_rate},
        metadata={"feature_columns": feature_columns, "contamination": contamination},
    )

    return {"anomaly_rate": anomaly_rate, "model_path": str(artifact_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a cluster-level anomaly detector.")
    parser.add_argument("--input-csv", type=str, required=True, help="Path to feature CSV.")
    parser.add_argument("--feature-columns", type=str, nargs="+", required=True, help="Feature columns.")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory to save the model artifact.")
    parser.add_argument("--contamination", type=float, default=0.05, help="Expected anomaly contamination.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    metrics = train_anomaly_model(
        input_csv=args.input_csv,
        feature_columns=args.feature_columns,
        output_dir=args.output_dir,
        contamination=args.contamination,
        random_state=args.seed,
    )
    LOGGER.info("Anomaly training complete: %s", metrics)


if __name__ == "__main__":
    main()
