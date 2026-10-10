"""Evaluation utilities for classification and regression tasks."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

LOGGER = logging.getLogger(__name__)


def compute_classification_metrics(
    y_true: list[int] | np.ndarray,
    y_pred: list[int] | np.ndarray,
    y_proba: np.ndarray | None = None,
) -> dict[str, float]:
    """Evaluate classification performance with standard metrics."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    metrics: dict[str, float] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
    if y_proba is not None:
        try:
            from sklearn.metrics import roc_auc_score

            metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba))
        except ValueError:
            LOGGER.warning("ROC AUC could not be computed for the supplied labels/probabilities.")
    return metrics


def compute_regression_metrics(y_true: list[float] | np.ndarray, y_pred: list[float] | np.ndarray) -> dict[str, float]:
    """Evaluate regression output using RMSE, MAE, and R2."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def summarize_metrics(results: dict[str, Any]) -> str:
    """Return a concise, human-readable metrics summary string."""
    summary_parts = []
    for key, value in results.items():
        if isinstance(value, float):
            summary_parts.append(f"{key}={value:.4f}")
        else:
            summary_parts.append(f"{key}={value}")
    return ", ".join(summary_parts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Evaluation utilities loaded.")
