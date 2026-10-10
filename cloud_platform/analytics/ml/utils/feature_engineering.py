"""Feature engineering utilities for temporal and spatial analytics."""

from __future__ import annotations

import logging

import geopandas as gpd
import pandas as pd

LOGGER = logging.getLogger(__name__)


def add_temporal_features(frame: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """Create standard temporal features such as hour, weekday, and month."""
    result = frame.copy()
    result[timestamp_col] = pd.to_datetime(result[timestamp_col], errors="coerce")
    result = result.dropna(subset=[timestamp_col]).copy()
    result["hour"] = result[timestamp_col].dt.hour
    result["day_of_week"] = result[timestamp_col].dt.dayofweek
    result["day_of_month"] = result[timestamp_col].dt.day
    result["month"] = result[timestamp_col].dt.month
    result["year"] = result[timestamp_col].dt.year
    return result


def add_lag_features(frame: pd.DataFrame, target_column: str, lags: list[int] | None = None) -> pd.DataFrame:
    """Append lag features for a target time series."""
    result = frame.copy()
    if target_column not in result.columns:
        raise ValueError(f"Target column '{target_column}' is missing.")
    for lag in lags or [1, 2, 3, 6, 12, 24]:
        result[f"{target_column}_lag_{lag}"] = result[target_column].shift(lag)
    return result


def aggregate_by_time_window(
    frame: pd.DataFrame,
    timestamp_col: str,
    value_columns: list[str],
    frequency: str = "H",
) -> pd.DataFrame:
    """Aggregate rows into a time window using pandas resample semantics."""
    result = frame.copy()
    result[timestamp_col] = pd.to_datetime(result[timestamp_col], errors="coerce")
    return result.set_index(timestamp_col)[value_columns].resample(frequency).mean().reset_index()


def build_spatial_features(
    frame: pd.DataFrame,
    latitude_col: str = "latitude",
    longitude_col: str = "longitude",
    borough_col: str = "borough",
) -> pd.DataFrame:
    """Create spatial features for borough or neighborhood-level analytics."""
    result = frame.copy()
    required = [latitude_col, longitude_col, borough_col]
    for column in required:
        if column not in result.columns:
            raise ValueError(f"Missing spatial column: {column}")

    try:
        gdf = gpd.GeoDataFrame(
            result,
            geometry=gpd.points_from_xy(result[longitude_col], result[latitude_col]),
            crs="EPSG:4326",
        )
        result["borough_code"] = result[borough_col].astype("category").cat.codes
        result["geo_point"] = gdf.geometry.to_wkt()
    except Exception as exc:
        LOGGER.warning("GeoPandas could not create spatial features; using fallback encoding. %s", exc)
        result["borough_code"] = result[borough_col].astype("category").cat.codes
        result["geo_point"] = None
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    LOGGER.info("Feature engineering utilities loaded.")
