"""Preprocessing utilities for ML pipelines."""

from __future__ import annotations

import logging
import os
import random
from typing import Any

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)


def set_deterministic_seed(seed: int | None = None) -> int:
    """Set deterministic seed across Python, NumPy, and PyTorch."""
    resolved_seed = int(seed or int(os.getenv("MODEL_SEED", "42")))
    random.seed(resolved_seed)
    np.random.seed(resolved_seed)
    torch.manual_seed(resolved_seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(resolved_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    return resolved_seed


def validate_required_columns(frame: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether a DataFrame contains required columns."""
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def normalize_numeric_columns(frame: pd.DataFrame, exclude_columns: list[str] | None = None) -> pd.DataFrame:
    """Standardize all numeric columns in a DataFrame."""
    result = frame.copy()
    exclude = set(exclude_columns or [])
    numeric_columns = [
        column for column in result.columns if pd.api.types.is_numeric_dtype(result[column]) and column not in exclude
    ]
    scaler = StandardScaler()
    result[numeric_columns] = scaler.fit_transform(result[numeric_columns])
    return result


def prepare_time_series_dataframe(
    frame: pd.DataFrame,
    timestamp_column: str,
    value_columns: list[str],
    sort: bool = True,
) -> pd.DataFrame:
    """Sanitize and order a time-series DataFrame."""
    validate_required_columns(frame, [timestamp_column] + value_columns)
    result = frame.copy()
    result[timestamp_column] = pd.to_datetime(result[timestamp_column], errors="coerce")
    result = result.dropna(subset=[timestamp_column])
    if sort:
        result = result.sort_values(timestamp_column).reset_index(drop=True)
    return result


def to_numpy_matrix(frame: pd.DataFrame, columns: list[str]) -> np.ndarray:
    """Convert selected columns to a NumPy matrix."""
    validate_required_columns(frame, columns)
    return frame[columns].to_numpy(dtype=float)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Preprocessing utility loaded.")
