from __future__ import annotations

import streamlit as st

from src.components.site_selector_v2 import render_site_selector_v2


def data_explorer() -> None:
    """Render the site selector v2 prototype."""
    with st.spinner("Loading geospatial data..."):
        render_site_selector_v2()
