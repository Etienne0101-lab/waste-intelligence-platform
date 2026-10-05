"""Tests for analytics pipelines."""

from cloud_platform.analytics.forecasting.facility_load import project_facility_load
from cloud_platform.analytics.histograms.temporal import build_temporal_histogram


def test_facility_load_forecast():
    history = [100.0, 110.0, 120.0, 130.0, 140.0]
    forecast = project_facility_load(history, horizon_days=7)
    assert forecast > 0


def test_temporal_histogram():
    events = [
        {"bucket": "hour_00", "value": 10.0},
        {"bucket": "hour_00", "value": 15.0},
        {"bucket": "hour_01", "value": 20.0},
    ]
    result = build_temporal_histogram(events)
    assert len(result["hour_00"]) == 2
    assert result["hour_00"] == [10.0, 15.0]
