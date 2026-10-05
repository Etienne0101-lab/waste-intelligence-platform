"""Reusable metric cards and dashboard widgets."""
from __future__ import annotations

import streamlit as st


def metric_card(label: str, value: float, unit: str = "", delta: float | None = None) -> None:
    if delta is not None:
        st.metric(label, f"{value:.2f} {unit}", delta=f"{delta:+.2f}")
    else:
        st.metric(label, f"{value:.2f} {unit}")


def facility_status_indicator(facility_id: str, utilization: float) -> None:
    if utilization > 90:
        color = "🔴"
        status = "Critical"
    elif utilization > 75:
        color = "🟡"
        status = "Warning"
    else:
        color = "🟢"
        status = "Optimal"
    st.write(f"{color} **{facility_id}**: {status} ({utilization:.1f}%)")
