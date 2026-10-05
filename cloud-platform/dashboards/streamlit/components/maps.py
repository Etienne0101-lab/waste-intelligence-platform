"""Geospatial map rendering components."""

from __future__ import annotations

import streamlit as st
from typing import List, Dict


def render_cluster_map(bins: List[Dict]) -> None:
    """Render an interactive map of bin clusters."""
    if not bins:
        st.info("No bin data available for mapping.")
        return

    # Create a simple map marker set
    map_data = [{"lat": b["latitude"], "lon": b["longitude"]} for b in bins]
    st.write(f"Map with {len(map_data)} bins")
    # In production, integrate with folium or plotly for interactive maps


def render_borough_summary(borough_data: Dict) -> None:
    """Render borough-level summary statistics."""
    st.subheader(f"{borough_data.get('borough', 'Unknown Borough')}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bins", borough_data.get("total_bins", 0))
    with col2:
        st.metric("Total Mass (kg)", f"{borough_data.get('total_mass_kg', 0):.1f}")
    with col3:
        st.metric("Diversion %", f"{borough_data.get('diversion_percent', 0):.1f}%")
