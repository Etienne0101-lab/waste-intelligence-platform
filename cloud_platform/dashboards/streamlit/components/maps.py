"""Map rendering helpers for streamlit dashboards."""
from __future__ import annotations

from typing import Dict, List

import streamlit as st


def render_cluster_map(bins: List[Dict]) -> None:
    if not bins:
        st.info("No bin data available for mapping.")
        return
    st.write(f"Map with {len(bins)} bins")


def render_borough_summary(borough_data: Dict) -> None:
    st.subheader(f"{borough_data.get('borough', 'Unknown Borough')}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bins", borough_data.get("total_bins", 0))
    with col2:
        st.metric("Total Mass (kg)", f"{borough_data.get('total_mass_kg', 0):.1f}")
    with col3:
        st.metric("Diversion %", f"{borough_data.get('diversion_percent', 0):.1f}%")
