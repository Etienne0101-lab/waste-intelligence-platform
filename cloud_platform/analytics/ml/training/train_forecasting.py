"""Train and save forecasting models for time-series waste predictions."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ..model_registry import ModelRegistry
from ..utils.feature_engineering import add_lag_features, add_temporal_features

LOGGER = logging.getLogger(__name__)


def train_forecasting_model(
    input_csv: str | Path,
    target: str,
    timestamp_col: str = "timestamp",
    id_col: str | None = None,
    output_dir: str | Path | None = None,
    horizon: int = 24,
    random_state: int = 42,
) -> dict[str, float | str]:
    """Train a forecasting model and save it in the model registry."""
    df = pd.read_csv(input_csv)
    if df.empty:
        raise ValueError("Input CSV is empty.")
    if timestamp_col not in df.columns:
        raise ValueError(f"Missing timestamp column: {timestamp_col}")
    if target not in df.columns:
        raise ValueError(f"Missing target column: {target}")

    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df = df.sort_values(timestamp_col).reset_index(drop=True)

    df = add_temporal_features(df, timestamp_col=timestamp_col)
    df = add_lag_features(df, target_column=target, lags=[1, 2, 3, 6, 12, 24])

    feature_columns = [
        column for column in df.columns if column not in {target, timestamp_col, id_col}
    ]
    if not feature_columns:
        raise ValueError("No forecast feature columns could be created.")

    split_index = max(1, int(len(df) * 0.8))
    train_df = df.iloc[:split_index]
    valid_df = df.iloc[split_index:]

    model = HistGradientBoostingRegressor(random_state=random_state)
    model.fit(train_df[feature_columns], train_df[target])

    predictions = model.predict(valid_df[feature_columns])
    rmse = mean_squared_error(valid_df[target], predictions, squared=False)
    mae = mean_absolute_error(valid_df[target], predictions)
    r2 = r2_score(valid_df[target], predictions)

    output_root = Path(output_dir or os.getenv("MODEL_STORAGE_PATH", "/models")) / "forecasting"
    output_root.mkdir(parents=True, exist_ok=True)
    artifact = output_root / f"forecast_model_{horizon}.joblib"
    joblib.dump(model, artifact)

    registry = ModelRegistry()
    registry.register_model(
        model_name="waste_forecast",
        model_type="sklearn",
        artifact_path=artifact,
        metrics={"rmse": float(rmse), "mae": float(mae), "r2": float(r2), "horizon": int(horizon)},
        metadata={"target": target, "timestamp_col": timestamp_col, "feature_columns": feature_columns},
    )
    return {"rmse": float(rmse), "mae": float(mae), "r2": float(r2), "model_path": str(artifact)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a forecasting model for waste analytics.")
    parser.add_argument("--input-csv", type=str, required=True, help="Path to input time-series CSV.")
    parser.add_argument("--target", type=str, required=True, help="Name of target variable.")
    parser.add_argument("--timestamp-col", type=str, default="timestamp", help="Timestamp column.")
    parser.add_argument("--id-col", type=str, default=None, help="Optional grouping ID column.")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory to save model artifact.")
    parser.add_argument("--horizon", type=int, default=24, help="Prediction horizon.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    metrics = train_forecasting_model(
        input_csv=args.input_csv,
        target=args.target,
        timestamp_col=args.timestamp_col,
        id_col=args.id_col,
        output_dir=args.output_dir,
        horizon=args.horizon,
        random_state=args.seed,
    )
    LOGGER.info("Forecasting training complete: %s", metrics)


if __name__ == "__main__":
    main()
