"""Prototype layout for the Yemen site selector v2 component with dataset metadata and map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import streamlit as st

from streamlit.components.v1 import html

# Site datasets metadata: location on disk, fields available for colouring, and detail attributes
SITE_DATASETS: Dict[str, Dict[str, Any]] = {
    "yeeap": {
        "label": "YEEAP installations",
        "path": Path("data/site_data/yeeap_installations.geojson"),
        "color_fields": [
            {"id": "pv_system_kwp", "label": "PV capacity (kWp)", "type": "numeric", "min": 0, "max": 75},
            {"id": "total_beneficiaries", "label": "Total beneficiaries", "type": "numeric", "min": 0, "max": 12_500},
            {"id": "is_completed", "label": "Completion status", "type": "categorical", "categories": ["In progress", "Completed"]},
            {"id": "category_level_1", "label": "Category", "type": "categorical"},
        ],
        "detail_fields": [
            {"id": "facility_name", "label": "Facility"},
            {"id": "category_level_1", "label": "Category"},
            {"id": "category_level_2", "label": "Sub-category"},
            {"id": "pv_system_kwp", "label": "PV capacity (kWp)"},
            {"id": "total_beneficiaries", "label": "Total beneficiaries"},
            {"id": "male_beneficiaries", "label": "Male beneficiaries"},
            {"id": "female_beneficiaries", "label": "Female beneficiaries"},
            {"id": "is_completed", "label": "Status"},
        ],
        "display": {
            "title_field": "facility_name",
            "subtitle_fields": ["category_level_1", "category_level_2"],
            "meta_field": "pv_system_kwp",
            "meta_label": "kWp",
        },
    },
    "tamkeen": {
        "label": "Tamkeen projects",
        "path": Path("data/site_data/tamkeen.geojson"),
        "color_fields": [
            {"id": "Status", "label": "Status", "type": "categorical", "categories": ["Planned", "Active", "Completed"]},
        ],
        "detail_fields": [
            {"id": "Subproject_ID", "label": "Subproject ID"},
            {"id": "Status", "label": "Status"},
            {"id": "Latitude", "label": "Latitude"},
            {"id": "Longitude", "label": "Longitude"},
        ],
        "display": {
            "title_field": "Subproject_ID",
            "subtitle_fields": ["Status"],
        },
    },
    "pilot_minigrid": {
        "label": "Pilot mini-grids",
        "path": Path("data/site_data/pilot_minigrid.geojson"),
        "color_fields": [
            {"id": "Estimated  Population", "label": "Estimated population", "type": "numeric", "min": 0, "max": 20_000},
            {"id": "Ownership", "label": "Ownership", "type": "categorical"},
        ],
        "detail_fields": [
            {"id": "name", "label": "Location"},
            {"id": "Estimated  Population", "label": "Estimated population"},
            {"id": "Ownership", "label": "Ownership"},
            {"id": "Latitude", "label": "Latitude"},
            {"id": "Longitude", "label": "Longitude"},
        ],
        "display": {
            "title_field": "name",
            "subtitle_fields": ["Ownership"],
            "meta_field": "Estimated  Population",
            "meta_label": "people",
        },
    },
    "health": {
        "label": "Health facilities",
        "path": Path("data/site_data/health_facilities.geojson"),
        "color_fields": [
            {"id": "amenity", "label": "Amenity type", "type": "categorical"},
            {"id": "healthcare", "label": "Healthcare type", "type": "categorical"},
        ],
        "detail_fields": [
            {"id": "name", "label": "Name"},
            {"id": "amenity", "label": "Amenity"},
        ],
        "display": {
            "title_field": "name",
            "subtitle_fields": ["amenity", "healthcare"],
        },
    },
    "education": {
        "label": "Education facilities",
        "path": Path("data/site_data/education_facilities.geojson"),
        "color_fields": [
            {"id": "amenity", "label": "Amenity type", "type": "categorical"},
        ],
        "detail_fields": [
            {"id": "name", "label": "Name"},
            {"id": "amenity", "label": "Amenity"},
        ],
        "display": {
            "title_field": "name",
            "subtitle_fields": ["amenity"],
        },
    },
}

GRID_FEATURE_CONFIG: Dict[str, Dict[str, Any]] = {
    "climate": {
        "label": "Climate hazard exposure",
        "path": Path("data/processed_h3/h3_climate_hazard_exposure.csv"),
        "labels": {
            "worldpop2023_sum": "WorldPop 2023 population",
            "adj_at_least_one": "Population exposed to ≥1 hazard",
            "adj_exposed_airpol15_pop": "Population exposed to PM₂.₅ ≥15",
            "adj_exposed_heat32_pop": "Population exposed to heat ≥32 °C",
            "adj_exposed_drought20_pop": "Population exposed to drought",
            "adj_exposed_flood5_pop": "Population exposed to flood",
        },
    },
    "education_access": {
        "label": "Education access",
        "path": Path("data/processed_h3/h3_education.csv"),
        "labels": {
            "education_number_of_sites": "Education site count",
            "education_distance_to_nearest_site_m": "Distance to education site (m)",
        },
    },
    "health_access": {
        "label": "Health access",
        "path": Path("data/processed_h3/h3_health.csv"),
        "labels": {
            "health_number_of_sites": "Health facility count",
            "health_distance_to_nearest_site_m": "Distance to health site (m)",
        },
    },
    "tamkeen_coverage": {
        "label": "Tamkeen coverage",
        "path": Path("data/processed_h3/h3_tamkeen.csv"),
        "labels": {
            "tamkeen_number_of_sites": "Tamkeen site count",
            "tamkeen_distance_to_nearest_site_m": "Distance to Tamkeen site (m)",
        },
    },
    "yeeap_coverage": {
        "label": "YEEAP coverage",
        "path": Path("data/processed_h3/h3_yeeap.csv"),
        "labels": {
            "yeeap_number_of_sites": "YEEAP installation count",
            "yeeap_distance_to_nearest_site_m": "Distance to YEEAP site (m)",
        },
    },
    "pti_indicators": {
        "label": "PTI indicators",
        "path": Path("data/processed_h3/h3_pti_indicators.csv"),
        "labels": {
            "pop_total": "Total population",
            "pop_density_per_km2": "Population density (/km²)",
            "total_idps_district": "IDPs (district)",
            "num_idp_hh_displaced_to_dtm_12m": "IDP HH displaced to district (12m)",
            "num_idp_hh_displaced_from_dtm_12m": "IDP HH displaced from district (12m)",
            "exposure_drought_pct": "Area exposed to drought (%)",
            "exposure_extreme_heat_pct": "Area exposed to extreme heat (%)",
            "exposure_flooding_pct": "Area exposed to flooding (%)",
            "conflict_incidents": "Conflict incidents",
            "conflict_fatalities": "Conflict fatalities",
            "ipc3_pct": "Population in IPC3+ (%)",
            "pct_wasted": "Wasting prevalence (%)",
            "pct_stunted_mod_sev": "Stunting prevalence (%)",
            "prim_school_walk_30m_plus_pct": "Primary students >30 min walk (%)",
            "sec_school_walk_30m_plus_pct": "Secondary students >30 min walk (%)",
            "num_schools_per_1000_children": "Schools per 1,000 children",
            "bemonc_walk_60m_plus_pct": "Births >60 min from BEmONC (%)",
            "num_health_facilities_per_10000": "Health facilities per 10k",
        },
    },
    "pti_scores": {
        "label": "PTI scores",
        "path": Path("data/processed_h3/h3_pti_scores.csv"),
        "labels": {
            "population_score": "Population score",
            "displacement_score": "Displacement score",
            "climate_score": "Climate score",
            "conflict_score": "Conflict score",
            "food_nutrition_security_score": "Food & nutrition score",
            "access_services_score": "Access to services score",
            "economic_activity_score": "Economic activity score",
        },
    },
}


@st.cache_data(ttl=3600)  # Cache for 1 hour
def _load_dataset_features(dataset_id: str) -> list[dict[str, Any]]:
    """Load and cache dataset features from GeoJSON files."""
    config = SITE_DATASETS[dataset_id]
    path = config["path"]
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        geojson = json.load(file)
    features: list[dict[str, Any]] = []
    for feature in geojson.get("features", []):
        geom = feature.get("geometry")
        props = feature.get("properties", {})
        if not geom or geom.get("type") != "Point":
            continue
        coords = geom.get("coordinates")
        if not isinstance(coords, (list, tuple)) or len(coords) < 2:
            continue
        lon, lat = coords[0], coords[1]
        features.append(
            {
                "id": props.get("id") or props.get("Subproject_ID") or props.get("name") or props.get("facility_name") or str(len(features)),
                "lat": lat,
                "lon": lon,
                "properties": props,
                "summary": "",
                "gridContext": {},
            }
        )
    return features


def _humanize_column(name: str) -> str:
    if not name:
        return ""
    label = name.replace("_", " ")
    label = label.replace("pct", "%")
    label = label.replace("per km2", "/km²")
    return label.title()


@st.cache_data(ttl=3600)  # Cache for 1 hour
def _load_grid_datasets() -> tuple[Dict[str, Any], Dict[str, Dict[str, Dict[str, float]]], Dict[str, Any]]:
    """Load and cache grid datasets (geometry, metadata, and values)."""
    base_path = Path("data/boundaries_h3/h3_grid_res5.geojson")
    with base_path.open("r", encoding="utf-8") as file:
        geometry = json.load(file)

    feature_sets_meta: Dict[str, Any] = {}
    feature_values: Dict[str, Dict[str, Dict[str, float]]] = {}

    for feature_id, config in GRID_FEATURE_CONFIG.items():
        path: Path = config["path"]
        if not path.exists():
            continue
        df = pd.read_csv(path)
        df = df.drop(columns=[col for col in df.columns if col.startswith("Unnamed")], errors="ignore")
        if "h3_05" not in df.columns:
            continue
        df = df.dropna(subset=["h3_05"]).copy()
        numeric_columns = []
        variables = []
        label_map = config.get("labels", {})

        for column in df.columns:
            if column == "h3_05":
                continue
            series = pd.to_numeric(df[column], errors="coerce")
            if not pd.api.types.is_numeric_dtype(series):
                continue
            series = series.dropna()
            if series.empty:
                continue
            col_min = float(series.min())
            col_max = float(series.max())
            label = label_map.get(column, _humanize_column(column))
            variables.append(
                {
                    "id": column,
                    "label": label,
                    "type": "numeric",
                    "min": col_min,
                    "max": col_max,
                }
            )
            numeric_columns.append(column)

        values_map: Dict[str, Dict[str, float]] = {}
        if numeric_columns:
            sub_df = df[["h3_05"] + numeric_columns].copy()
            for column in numeric_columns:
                sub_df[column] = pd.to_numeric(sub_df[column], errors="coerce")
            for h3, row in sub_df.set_index("h3_05").iterrows():
                values_map[h3] = {
                    column: (None if pd.isna(value) else float(value))
                    for column, value in row.items()
                }

        feature_sets_meta[feature_id] = {
            "label": config["label"],
            "path": str(path),
            "variables": variables,
        }
        feature_values[feature_id] = values_map

    return {"feature_sets": feature_sets_meta}, feature_values, geometry

@st.cache_data(ttl=3600)
def render_site_selector_v2() -> None:
    """Render a three-column prototype for the site selector v2 dashboard."""
    
    # Use session state to cache JSON strings to avoid re-serialization
    cache_key_data = "site_selector_data_cache"
    cache_key_grid = "site_selector_grid_cache"
    
    # Check if we have cached JSON strings
    if cache_key_data not in st.session_state or cache_key_grid not in st.session_state:
        # Load data (cached functions, so fast after first load)
        datasets_json = json.dumps({k: {**v, "path": str(v["path"])} for k, v in SITE_DATASETS.items()})
        
        # Load features for all datasets
        features_dict = {}
        for dataset_id in SITE_DATASETS:
            features_dict[dataset_id] = _load_dataset_features(dataset_id)
        features_json = json.dumps(features_dict)
        
        # Load grid data
        grid_meta, grid_values, grid_geometry = _load_grid_datasets()
        grid_datasets_json = json.dumps(grid_meta)
        grid_values_json = json.dumps(grid_values)
        grid_geometry_json = json.dumps(grid_geometry)
        
        # Cache the JSON strings in session state
        st.session_state[cache_key_data] = {
            "datasets_json": datasets_json,
            "features_json": features_json,
        }
        st.session_state[cache_key_grid] = {
            "grid_datasets_json": grid_datasets_json,
            "grid_values_json": grid_values_json,
            "grid_geometry_json": grid_geometry_json,
        }
    else:
        # Use cached JSON strings
        datasets_json = st.session_state[cache_key_data]["datasets_json"]
        features_json = st.session_state[cache_key_data]["features_json"]
        grid_datasets_json = st.session_state[cache_key_grid]["grid_datasets_json"]
        grid_values_json = st.session_state[cache_key_grid]["grid_values_json"]
        grid_geometry_json = st.session_state[cache_key_grid]["grid_geometry_json"]

    template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Site Selector v2 Prototype</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
      :root {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #e2e8f0;
        background: #050914;
      }
      *, *::before, *::after {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        height: 100vh;
        overflow: hidden;
        background: radial-gradient(circle at 12% -8%, rgba(91, 99, 244, 0.35), transparent 55%);
      }
      .app {
        display: grid;
        grid-template-columns: 360px minmax(600px, 1fr) 340px;
        gap: 1.6rem;
        padding: 1.6rem 1.8rem;
        height: 100%;
      }
      .panel {
        display: flex;
        flex-direction: column;
        border-radius: 24px;
        background: rgba(13, 20, 42, 0.92);
        backdrop-filter: blur(16px);
        box-shadow: 0 30px 45px -26px rgba(3, 7, 18, 0.7);
        min-height: 0;
      }
      .panel header {
        padding: 1.3rem 1.5rem 1rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
      }
      .panel header h2 {
        margin: 0;
        font-size: 1.25rem;
      }
      .panel header p {
        margin: 0.35rem 0 0;
        font-size: 0.9rem;
        color: #8fb5ff;
      }
      .panel__body {
        flex: 1;
        overflow-y: auto;
        padding: 1.2rem 1.5rem 1.5rem;
        display: grid;
        gap: 1.1rem;
      }
      .section {
        display: grid;
        gap: 0.75rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 18px;
        padding: 1rem 1.1rem;
      }
      .section h3 {
        margin: 0;
        font-size: 0.95rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: rgba(186, 201, 255, 0.85);
      }
      label {
        display: grid;
        gap: 0.4rem;
        font-size: 0.9rem;
      }
      select, input[type="number"] {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.32);
        background: rgba(8, 13, 30, 0.85);
        color: inherit;
        padding: 0.55rem 0.75rem;
        font-size: 0.9rem;
      }
      select:focus, input[type="number"]:focus {
        outline: 2px solid rgba(99, 179, 237, 0.45);
      }
      .legend {
        font-size: 0.82rem;
        color: rgba(226, 232, 240, 0.7);
        display: flex;
        justify-content: space-between;
      }
      .marker-control {
        display: grid;
        gap: 0.45rem;
        font-size: 0.82rem;
      }
      .marker-control input[type="range"] {
        width: 100%;
      }
      .styling-panel {
        padding: 0;
        background: transparent !important;
        border: none !important;
      }
      .styling-panel summary {
        list-style: none;
      }
      .styling-panel summary::-webkit-details-marker {
        display: none;
      }
      .styling-panel summary::before {
        content: "▶";
        display: inline-block;
        margin-right: 0.5rem;
        transition: transform 0.2s ease;
        font-size: 0.7rem;
      }
      .styling-panel[open] summary::before {
        transform: rotate(90deg);
      }
      .styling-controls {
        display: grid;
        gap: 0.9rem;
      }
      .styling-control-item {
        display: grid;
        gap: 0.4rem;
      }
      .selector-note {
        margin: 0;
        font-size: 0.82rem;
        color: rgba(226, 232, 240, 0.68);
      }
      details {
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: rgba(9, 14, 25, 0.75);
        padding: 0.75rem 0.9rem;
      }
      details summary {
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
      }
      details ul {
        margin: 0.8rem 0 0;
        padding-left: 1.1rem;
        display: grid;
        gap: 0.4rem;
        font-size: 0.85rem;
      }
      .tabs {
        display: flex;
        gap: 0.6rem;
        padding: 0.8rem 1.2rem 0;
      }
      .tab {
        flex: 1;
        border-radius: 14px;
        text-align: center;
        padding: 0.6rem 0.8rem;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid transparent;
        background: rgba(255, 255, 255, 0.05);
        transition: all 0.15s ease;
      }
      .tab[data-active="true"] {
        background: rgba(91, 99, 244, 0.3);
        border-color: rgba(91, 99, 244, 0.6);
      }
      .map-container, .need-container {
        flex: 1;
        margin: 0 1.2rem 1.2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: radial-gradient(circle at center, rgba(28, 58, 138, 0.92), rgba(7, 10, 22, 0.92));
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(226, 232, 240, 0.75);
        position: relative;
        padding: 1.2rem;
      }
      #map-root {
        position: absolute;
        inset: 0;
        border-radius: 18px;
        overflow: hidden;
        z-index: 1;
      }
      .map-site-legend {
        position: absolute;
        right: 1.3rem;
        bottom: 1.3rem;
        background: rgba(8, 13, 30, 0.78);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.28);
        padding: 1rem 1.1rem;
        min-width: 240px;
        font-size: 0.85rem;
        display: grid;
        gap: 0.8rem;
        z-index: 4;
      }
      .map-site-legend.hidden {
        display: none;
      }
      .map-grid-legend {
        position: absolute;
        left: 1.3rem;
        bottom: 1.3rem;
        background: rgba(8, 13, 30, 0.78);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.28);
        padding: 1rem 1.1rem;
        min-width: 240px;
        font-size: 0.85rem;
        display: grid;
        gap: 0.8rem;
        z-index: 4;
      }
      .map-grid-legend.hidden {
        display: none;
      }
      .map-legend-header {
        display: grid;
        gap: 0.35rem;
      }
      .map-legend-header span {
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: rgba(148, 163, 184, 0.85);
      }
      .map-legend-header strong {
        font-size: 0.95rem;
      }
      .map-legend-title {
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: rgba(148, 163, 184, 0.85);
      }
      .map-legend-gradient {
        display: grid;
        gap: 0.4rem;
      }
      .map-legend-gradient-bar {
        height: 12px;
        border-radius: 999px;
        background: linear-gradient(90deg, #5b63f4 0%, #ef4444 100%);
        border: 1px solid rgba(148, 163, 184, 0.25);
      }
      .map-legend-gradient-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        color: rgba(226, 232, 240, 0.75);
      }
      .map-legend-items {
        display: grid;
        gap: 0.35rem;
      }
      .map-legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.82rem;
      }
      .grid-tooltip {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.85rem !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        pointer-events: none !important;
      }
      .map-legend-swatch {
        width: 14px;
        height: 14px;
        border-radius: 4px;
        border: 1px solid rgba(148, 163, 184, 0.35);
      }
      .need-layout {
        width: 100%;
        display: grid;
        grid-template-columns: minmax(260px, 320px) 1fr;
        gap: 1.2rem;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
      }
      thead {
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: rgba(148, 163, 184, 0.85);
      }
      th, td {
        text-align: left;
        padding: 0.4rem 0.35rem;
      }
      tbody tr:nth-child(odd) {
        background: rgba(255, 255, 255, 0.04);
      }
      button {
        border-radius: 14px;
        border: none;
        padding: 0.65rem 1rem;
        font-weight: 600;
        font-size: 0.93rem;
        cursor: pointer;
        background: #5b63f4;
        color: #f8fafc;
        margin-top: 0.8rem;
      }
      button:hover {
        background: #4f54d6;
      }
      .analytics-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 18px;
        padding: 1rem;
        display: grid;
        gap: 0.9rem;
      }
      .detail-section {
        padding: 1.1rem 1.4rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.16);
      }
      .detail-section:last-child {
        border-bottom: none;
      }
      .detail-section h3 {
        margin: 0 0 0.4rem;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: rgba(186, 201, 255, 0.85);
      }
      .kv-list {
        display: grid;
        gap: 0.45rem;
      }
      .kv {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 0.4rem;
        font-size: 0.88rem;
      }
      .kv span.label {
        color: rgba(148, 163, 184, 0.85);
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-size: 0.75rem;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.3rem 0.7rem;
        background: rgba(91, 99, 244, 0.2);
        color: #cbd5ff;
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }
      .site-list {
        display: grid;
        gap: 0.7rem;
      }
      .site-card {
        border-radius: 16px;
        padding: 0.75rem 0.9rem;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid transparent;
        cursor: pointer;
        display: grid;
        gap: 0.25rem;
        transition: transform 0.15s ease, border 0.15s ease;
      }
      .site-card[data-selected="true"] {
        border-color: rgba(255, 255, 255, 0.45);
        transform: translateY(-2px);
      }
      .site-card h4 {
        margin: 0;
        font-size: 0.98rem;
      }
      .site-card p {
        margin: 0;
        font-size: 0.82rem;
        color: rgba(226, 232, 240, 0.75);
      }
      .search {
        margin-bottom: 1rem;
      }
      .search input {
        width: 100%;
        padding: 0.6rem 0.9rem;
        font-size: 0.95rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.1);
        color: inherit;
        outline: none;
      }
      .empty-state {
        padding: 1rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        font-size: 0.85rem;
        color: rgba(226, 232, 240, 0.7);
      }
      .selector-note {
        font-size: 0.85rem;
        color: rgba(226, 232, 240, 0.7);
        margin-top: 0.5rem;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="app" data-state="map">
      <section class="panel" id="controls-panel">
        <header>
          <h2>Data & Layer Controls</h2>
          <p>Select a site dataset, choose styling variables, and configure grid overlays.</p>
        </header>
        <div class="panel__body">
          <div class="section" id="site-selector">
            <h3>Site dataset</h3>
            <label>
              Dataset
              <select id="site-dataset"></select>
            </label>
            <label>
              Colour by
              <select id="site-variable"></select>
            </label>
            
            <!-- Site Styling Controls -->
            <details class="styling-panel" style="margin-top: 0.75rem;">
              <summary style="cursor: pointer; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase; color: rgba(186, 201, 255, 0.85); font-weight: 600; padding: 0.5rem 0; list-style: none;">
                Site Styling
              </summary>
              <div class="styling-controls" style="margin-top: 0.75rem;">
                <div class="styling-control-item">
                  <label for="toggle-sites" style="font-size: 0.82rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                    <input id="toggle-sites" type="checkbox" checked style="cursor: pointer;" />
                    <span>Show sites</span>
                  </label>
                </div>
                <div class="styling-control-item">
                  <label for="color-map" style="font-size: 0.82rem; display: grid; gap: 0.4rem;">
                    <span>Color scheme</span>
                    <select id="color-map" style="width: 100%;"></select>
                  </label>
                </div>
                <div class="styling-control-item">
                  <label for="marker-size" style="font-size: 0.82rem; display: grid; gap: 0.4rem;">
                    <span>Size</span>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                      <input id="marker-size" type="range" min="1" max="18" step="1" value="1" style="flex: 1;" />
                      <span id="marker-size-value" style="min-width: 2rem; text-align: right; font-size: 0.85rem; color: rgba(226, 232, 240, 0.8);">3</span>
                    </div>
                  </label>
                </div>
              </div>
            </details>
          </div>

          <div class="section" id="grid-selector">
            <h3>Grid layer</h3>
            <label>
              Layer
              <select id="grid-layer"></select>
            </label>
            <label>
              Metric
              <select id="grid-variable"></select>
            </label>
            <label style="font-size:0.82rem;align-items:center;gap:0.5rem;display:flex;margin-top:0.5rem;">
              <input id="toggle-log-scale" type="checkbox" />
              <span>Scale with log(1-p)</span>
            </label>
            <div class="legend" id="grid-legend">
              <span>Min —</span>
              <span>Max —</span>
            </div>
            <label style="font-size:0.82rem;align-items:center;gap:0.5rem;display:flex;">
              <input id="toggle-grid" type="checkbox" checked />
              Show grid overlay
            </label>
            <label style="font-size:0.82rem;align-items:center;gap:0.5rem;display:flex;">
              <input id="toggle-need" type="checkbox" />
              Enable derived need & opportunity layer
            </label>
          </div>
        </div>
      </section>

      <section class="panel" id="analysis-panel">
        <header>
          <h2>Spatial Analysis</h2>
          <p>Map views and derived Need & Opportunity analytics.</p>
        </header>
        <div class="tabs">
          <div class="tab" data-tab="map" data-active="true">Map view</div>
          <div class="tab" data-tab="need">Need & Opportunity</div>
        </div>
        <div class="map-container" id="map-container">
          <div id="map-root"></div>
          <div class="map-site-legend hidden" id="map-site-legend"></div>
          <div class="map-grid-legend hidden" id="map-grid-legend"></div>
        </div>
        <div class="need-container" id="need-view" style="display:none;">
          <div class="need-layout">
            <div>
              <h3 style="margin:0 0 0.8rem;font-size:1rem;">Weight configuration</h3>
              <table>
                <thead>
                  <tr>
                    <th>PTI score</th>
                    <th>Need</th>
                    <th>Opportunity</th>
                  </tr>
                </thead>
                <tbody id="weights-table"></tbody>
              </table>
              <button id="recompute-btn">Generate scores</button>
              <p id="score-summary" style="margin:0.7rem 0 0;font-size:0.85rem;color:rgba(226,232,240,0.75);">
                Need: 0.00 • Opportunity: 0.00 • Combined: 0.00
              </p>
            </div>
            <div class="analytics-card">
              <div>
                <h4 style="margin:0 0 0.4rem;font-size:0.95rem;">Need vs Opportunity</h4>
                <div id="scatter-placeholder" style="height:180px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.04);border-radius:12px;">
                  Scatter plot placeholder
                </div>
              </div>
              <div>
                <h4 style="margin:0 0 0.4rem;font-size:0.95rem;">Combined score distribution</h4>
                <div id="hist-placeholder" style="height:160px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.04);border-radius:12px;">
                  Histogram placeholder
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="panel" id="detail-panel">
        <header>
          <h2>Selection Details</h2>
          <p>Contextual information for the active site or grid cell.</p>
        </header>
        <div class="panel__body" style="padding:1.1rem 0 0;">
          <div class="detail-section" id="detail-header">
            <div class="pill" id="detail-type">Site</div>
            <h3 id="detail-title" style="margin-top:0.6rem;font-size:1.05rem;letter-spacing:0;">–</h3>
            <p id="detail-subtitle" style="margin:0.35rem 1.4rem 0;font-size:0.9rem;color:rgba(226,232,240,0.75);">
              Select a site to view attributes.
            </p>
          </div>
          <div class="detail-section" id="detail-core">
            <h3>Site attributes</h3>
            <div class="kv-list" id="site-attributes"></div>
          </div>
          <div class="detail-section" id="detail-grid">
            <h3>H3 context</h3>
            <div class="kv-list" id="grid-attributes"></div>
          </div>
        </div>
      </section>
    </div>

    <script id="site-datasets-data" type="application/json">__SITE_DATASETS__</script>
    <script id="site-features-data" type="application/json">__SITE_FEATURES__</script>
    <script id="grid-datasets-data" type="application/json">__GRID_DATASETS__</script>
    <script id="grid-values-data" type="application/json">__GRID_VALUES__</script>
    <script id="grid-geometry-data" type="application/json">__GRID_GEOMETRY__</script>

    <script>
      const SITE_DATASETS = JSON.parse(document.getElementById("site-datasets-data").textContent);
      const SITE_FEATURES = JSON.parse(document.getElementById("site-features-data").textContent);
      const GRID_DATASETS_META = JSON.parse(document.getElementById("grid-datasets-data").textContent);
      const GRID_VALUES = JSON.parse(document.getElementById("grid-values-data").textContent);
      const GRID_GEOMETRY = JSON.parse(document.getElementById("grid-geometry-data").textContent);
      const GRID_LAYERS = Object.entries(GRID_DATASETS_META.feature_sets).map(([id, config]) => ({
        id,
        name: config.label,
        path: config.path,
        variables: config.variables,
      }));

      const PTI_SCORES = [
        { id: "population_score", label: "Population pressure" },
        { id: "displacement_score", label: "Displacement" },
        { id: "climate_score", label: "Climate exposure" },
        { id: "conflict_score", label: "Conflict" },
        { id: "food_nutrition_security_score", label: "Food & nutrition" },
        { id: "access_services_score", label: "Access to services" },
        { id: "economic_activity_score", label: "Economic activity" },
      ];

      const CATEGORY_COLORS = [
        "#5b63f4",
        "#22d3ee",
        "#34d399",
        "#facc15",
        "#f97316",
        "#f472b6",
        "#14b8a6",
        "#ef4444",
        "#a855f7",
        "#0ea5e9",
      ];

      const COLOR_MAPS = {
        continuous: [
          { id: "blue-red", name: "Blue to Red", start: [91, 99, 244], end: [239, 68, 68] },
          { id: "viridis", name: "Viridis", start: [68, 1, 84], end: [253, 231, 37] },
          { id: "plasma", name: "Plasma", start: [13, 8, 135], end: [240, 249, 33] },
          { id: "green-blue", name: "Green to Blue", start: [34, 211, 153], end: [14, 165, 233] },
          { id: "purple-orange", name: "Purple to Orange", start: [168, 85, 247], end: [249, 115, 22] },
        ],
        categorical: [
          { id: "default", name: "Default", colors: CATEGORY_COLORS },
          { id: "pastel", name: "Pastel", colors: ["#a8e6cf", "#ffd3b6", "#ffaaa5", "#ff8b94", "#c7ceea", "#b4a7d6", "#dda0dd", "#98d8c8"] },
          { id: "bright", name: "Bright", colors: ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#f0932b", "#eb4d4b", "#6c5ce7", "#a29bfe"] },
          { id: "earth", name: "Earth tones", colors: ["#8b4513", "#cd853f", "#daa520", "#b8860b", "#9acd32", "#6b8e23", "#556b2f", "#2f4f2f"] },
        ],
      };

      function toNumber(value) {
        if (value === null || value === undefined || value === "") return null;
        const num = Number(value);
        return Number.isFinite(num) ? num : null;
      }

      function getFeatureValue(feature, variable) {
        if (!variable) return null;
        const raw = feature?.properties?.[variable.id];
        if (raw === undefined || raw === null || raw === "") return null;
        return variable.type === "numeric" ? toNumber(raw) : String(raw);
      }

      function computeLegendData(features, variable, colorMapId) {
        if (!variable) return null;
        if (variable.type === "categorical") {
          const seen = new Map();
          const categories = [];
          const map = COLOR_MAPS.categorical.find(m => m.id === colorMapId) || COLOR_MAPS.categorical[0];
          const colors = map.colors || CATEGORY_COLORS;
          const register = (value) => {
            const key = value === null || value === undefined || value === "" ? "Unknown" : String(value);
            if (seen.has(key) || categories.length >= colors.length) {
              return;
            }
            const color = colors[categories.length % colors.length];
            const entry = { value: key, color };
            seen.set(key, entry);
            categories.push(entry);
          };
          features.forEach((feature) => register(feature?.properties?.[variable.id]));
          if (!categories.length) {
            register("Unknown");
          }
          return { type: "categorical", categories, colorMap: Object.fromEntries(categories.map((entry) => [entry.value, entry.color])) };
        }
        let min = Infinity;
        let max = -Infinity;
        features.forEach((feature) => {
          const value = toNumber(feature?.properties?.[variable.id]);
          if (value === null) return;
          if (value < min) min = value;
          if (value > max) max = value;
        });
        if (!Number.isFinite(min) || !Number.isFinite(max)) {
          return null;
        }
        if (min === max) {
          max = min + 1;
        }
        return { type: "numeric", min, max };
      }

      function applyLogScale(value) {
        if (value === null || value === undefined) return null;
        const numValue = toNumber(value);
        if (numValue === null || !Number.isFinite(numValue)) return null;
        // Apply log(1-p) transformation: log(1 + value) to handle zeros
        // Using log(1 + value) as standard approach for zero-handling
        if (numValue < 0) return null; // Can't log negative values in this context
        return Math.log(1 + numValue);
      }

      function computeLegendDataFromGrid(valuesMap, variable, useLogScale = false) {
        if (!variable) return null;
        if (variable.type === "categorical") {
          const seen = new Map();
          const categories = [];
          Object.values(valuesMap).forEach((row) => {
            const value = row?.[variable.id];
            const key = value === null || value === undefined || value === "" ? "Unknown" : String(value);
            if (seen.has(key) || categories.length >= CATEGORY_COLORS.length) {
              return;
            }
            const color = CATEGORY_COLORS[categories.length % CATEGORY_COLORS.length];
            const entry = { value: key, color };
            seen.set(key, entry);
            categories.push(entry);
          });
          if (!categories.length) {
            const entry = { value: "Unknown", color: CATEGORY_COLORS[0] };
            categories.push(entry);
            seen.set("Unknown", entry);
          }
          return { type: "categorical", categories, colorMap: Object.fromEntries(categories.map((entry) => [entry.value, entry.color])) };
        }
        let min = Infinity;
        let max = -Infinity;
        let originalMin = Infinity;
        let originalMax = -Infinity;
        Object.values(valuesMap).forEach((row) => {
          const originalValue = toNumber(row?.[variable.id]);
          if (originalValue === null) return;
          // Track original values
          if (originalValue < originalMin) originalMin = originalValue;
          if (originalValue > originalMax) originalMax = originalValue;
          // Transform for color calculation
          let value = originalValue;
          if (useLogScale) {
            value = applyLogScale(value);
            if (value === null) return;
          }
          if (value < min) min = value;
          if (value > max) max = value;
        });
        if (!Number.isFinite(min) || !Number.isFinite(max)) {
          originalMin = toNumber(variable.min);
          originalMax = toNumber(variable.max);
          min = originalMin;
          max = originalMax;
          if (useLogScale && Number.isFinite(min) && Number.isFinite(max)) {
            min = applyLogScale(min);
            max = applyLogScale(max);
          }
        }
        if (!Number.isFinite(min) || !Number.isFinite(max)) {
          return null;
        }
        if (min === max) {
          max = min + 1;
        }
        // If we didn't find original values from data, use variable metadata
        if (!Number.isFinite(originalMin) || !Number.isFinite(originalMax)) {
          originalMin = toNumber(variable.min);
          originalMax = toNumber(variable.max);
        }
        return { type: "numeric", min, max, originalMin, originalMax, useLogScale };
      }

      function updateGridLegendPanel(legend, layerMeta, variable) {
        if (!mapGridLegend) return;
        if (!legend || !variable || !state.showGrid) {
          mapGridLegend.classList.add("hidden");
          mapGridLegend.innerHTML = "";
          return;
        }
        mapGridLegend.classList.remove("hidden");
        const datasetLabel = layerMeta?.name ?? "Grid layer";
        const variableLabel = variable?.label ?? "Variable";
        if (legend.type === "numeric") {
          // Use original values for display if log scale is applied
          const displayMin = legend.originalMin !== undefined ? legend.originalMin : legend.min;
          const displayMax = legend.originalMax !== undefined ? legend.originalMax : legend.max;
          mapGridLegend.innerHTML = `
            <div class="map-legend-header">
              <span>${datasetLabel}</span>
              <strong>${variableLabel}</strong>
            </div>
            <div class="map-legend-title">Legend</div>
            <div class="map-legend-gradient">
              <div class="map-legend-gradient-bar"></div>
              <div class="map-legend-gradient-labels">
                <span>${formatLegendValue(displayMin)}</span>
                <span>${formatLegendValue(displayMax)}</span>
              </div>
            </div>
          `;
        } else {
          const items = legend.categories
            .map((entry) => `
              <div class="map-legend-item">
                <span class="map-legend-swatch" style="background:${entry.color};"></span>
                <span>${entry.value}</span>
              </div>
            `)
            .join("");
          mapGridLegend.innerHTML = `
            <div class="map-legend-header">
              <span>${datasetLabel}</span>
              <strong>${variableLabel}</strong>
            </div>
            <div class="map-legend-title">Legend</div>
            <div class="map-legend-items">${items}</div>
          `;
        }
      }

      function interpolateColor(t, colorMap) {
        const clamp = Math.min(1, Math.max(0, t));
        const start = colorMap?.start || [91, 99, 244];
        const end = colorMap?.end || [239, 68, 68];
        const channel = (index) => Math.round(start[index] + (end[index] - start[index]) * clamp);
        return `rgb(${channel(0)}, ${channel(1)}, ${channel(2)})`;
      }

      function colorForValue(value, legend, colorMapId) {
        if (!legend) {
          return "#000000";
        }
        if (legend.type === "numeric") {
          if (value === null) return "#94a3b8";
          const t = (value - legend.min) / (legend.max - legend.min);
          const map = COLOR_MAPS.continuous.find(m => m.id === colorMapId) || COLOR_MAPS.continuous[0];
          return interpolateColor(t, map);
        }
        const key = value === null || value === undefined || value === "" ? "Unknown" : String(value);
        const map = COLOR_MAPS.categorical.find(m => m.id === colorMapId) || COLOR_MAPS.categorical[0];
        const colorIndex = legend.categories.findIndex(c => c.value === key);
        if (colorIndex >= 0 && map.colors) {
          return map.colors[colorIndex % map.colors.length];
        }
        return legend.colorMap?.[key] || "#94a3b8";
      }

      function updateLegend(legend, variable, colorMapId) {
        if (!mapLegend) return;
        const dataset = getActiveDataset();
        const variableLabel = variable ? variable.label : "None";
        mapLegend.classList.remove("hidden");
        if (!legend || !variable) {
          mapLegend.innerHTML = `
            <div class="map-legend-header">
              <span>${dataset?.label ?? "Sites"}</span>
              <strong>${variableLabel}</strong>
            </div>
            <div class="map-legend-title">Legend</div>
            <div class="empty-state" style="background:rgba(255,255,255,0.04);border-radius:12px;padding:0.5rem;text-align:center;">No color mapping</div>
          `;
          return;
        }
        if (legend.type === "numeric") {
          const map = COLOR_MAPS.continuous.find(m => m.id === colorMapId) || COLOR_MAPS.continuous[0];
          const startColor = `rgb(${map.start[0]}, ${map.start[1]}, ${map.start[2]})`;
          const endColor = `rgb(${map.end[0]}, ${map.end[1]}, ${map.end[2]})`;
          mapLegend.innerHTML = `
            <div class="map-legend-header">
              <span>${dataset.label}</span>
              <strong>${variableLabel}</strong>
            </div>
            <div class="map-legend-title">Legend</div>
            <div class="map-legend-gradient">
              <div class="map-legend-gradient-bar" style="background: linear-gradient(90deg, ${startColor} 0%, ${endColor} 100%);"></div>
              <div class="map-legend-gradient-labels">
                <span>${formatLegendValue(legend.min)}</span>
                <span>${formatLegendValue(legend.max)}</span>
              </div>
            </div>
          `;
        } else {
          const items = legend.categories
            .map((entry) => `
              <div class="map-legend-item">
                <span class="map-legend-swatch" style="background:${entry.color};"></span>
                <span>${entry.value}</span>
              </div>
            `)
            .join("");
          mapLegend.innerHTML = `
            <div class="map-legend-header">
              <span>${dataset.label}</span>
              <strong>${variableLabel}</strong>
            </div>
            <div class="map-legend-title">Legend</div>
            <div class="map-legend-items">${items}</div>
          `;
        }
      }

      const datasetIds = Object.keys(SITE_DATASETS);
      const initialDatasetId = datasetIds[0];
      const initialDatasetConfig = SITE_DATASETS[initialDatasetId];

      const state = {
        siteDataset: initialDatasetId,
        siteVariable: "__none__",
        gridLayer: GRID_LAYERS[0].id,
        gridVariable: GRID_LAYERS[0].variables[0].id,
        features: SITE_FEATURES[initialDatasetId] || [],
        selectedIndex: 0,
        markerSize: 3,
        showSites: true,
        showGrid: true,
        colorMap: "blue-red",
        useLogScale: false,
        gridMeta: GRID_DATASETS_META,
        weights: PTI_SCORES.reduce((acc, item) => {
          acc[item.id] = {
            need: item.id === "population_score" || item.id === "displacement_score" ? 1 : 0,
            opp: item.id === "access_services_score" || item.id === "economic_activity_score" ? 1 : 0,
          };
          return acc;
        }, {}),
      };

      const siteDatasetSelect = document.getElementById("site-dataset");
      const siteVariableSelect = document.getElementById("site-variable");
      const colorMapSelect = document.getElementById("color-map");
      const toggleSites = document.getElementById("toggle-sites");
      const markerSizeValue = document.getElementById("marker-size-value");
      const siteLegend = document.getElementById("site-legend");
      const gridLayerSelect = document.getElementById("grid-layer");
      const gridVariableSelect = document.getElementById("grid-variable");
      const gridLegend = document.getElementById("grid-legend");
      const toggleGrid = document.getElementById("toggle-grid");
      const toggleNeed = document.getElementById("toggle-need");
      const toggleLogScale = document.getElementById("toggle-log-scale");
      const tabButtons = document.querySelectorAll(".tab");
      const mapContainer = document.getElementById("map-container");
      const mapLegend = document.getElementById("map-site-legend");
      const mapGridLegend = document.getElementById("map-grid-legend");
      const markerSizeInput = document.getElementById("marker-size");
      const weightsTable = document.getElementById("weights-table");
      const scoreSummary = document.getElementById("score-summary");
      const detailType = document.getElementById("detail-type");
      const detailTitle = document.getElementById("detail-title");
      const detailSubtitle = document.getElementById("detail-subtitle");
      const siteAttributesEl = document.getElementById("site-attributes");
      const gridAttributesEl = document.getElementById("grid-attributes");

      if (markerSizeInput) {
        markerSizeInput.value = state.markerSize;
        markerSizeInput.min = 1;
        markerSizeInput.max = 18;
        if (markerSizeValue) {
          markerSizeValue.textContent = state.markerSize;
        }
      }
      if (toggleSites) {
        toggleSites.checked = state.showSites;
      }
      if (toggleGrid) {
        toggleGrid.checked = state.showGrid;
      }

      let map = null;
      let markersLayer = null;
      let gridOverlayLayer = null;

      function getActiveDataset() {
        return SITE_DATASETS[state.siteDataset];
      }

      function getActiveSiteVariable() {
        if (state.siteVariable === "__none__" || !state.siteVariable) {
          return null;
        }
        const dataset = getActiveDataset();
        return dataset.color_fields.find((field) => field.id === state.siteVariable) ?? null;
      }

      function formatLegend(variable) {
        if (!variable) return ["–", "–"];
        if (variable.type === "categorical") {
          const size = variable.categories ? variable.categories.length : "";
          return ["Categorical", size ? `${size} values` : "—"];
        }
        const formatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: variable.max > 10 ? 0 : 2 });
        return [formatter.format(variable.min ?? 0), formatter.format(variable.max ?? 0)];
      }

      function formatLegendValue(value) {
        if (value === null || value === undefined) return "—";
        if (typeof value === "number") {
          const formatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: Math.abs(value) < 1 ? 2 : 0 });
          return formatter.format(value);
        }
        return String(value);
      }

      function renderSiteSelectors() {
        siteDatasetSelect.innerHTML = datasetIds
          .map((id) => `<option value="${id}">${SITE_DATASETS[id].label}</option>`)
          .join("");
        siteDatasetSelect.value = state.siteDataset;
        updateSiteVariables();
      }

      function updateSiteVariables() {
        const dataset = getActiveDataset();
        siteVariableSelect.innerHTML = `<option value="__none__">None</option>` + dataset.color_fields
          .map((variable) => `<option value="${variable.id}">${variable.label}</option>`)
          .join("");
        if (state.siteVariable === "__none__" || !dataset.color_fields.find((field) => field.id === state.siteVariable)) {
          state.siteVariable = "__none__";
        }
        siteVariableSelect.value = state.siteVariable ?? "__none__";
        const variable = getActiveSiteVariable();
        updateColorMapOptions(variable);
      }

      function updateColorMapOptions(variable) {
        if (!colorMapSelect) return;
        if (!variable) {
          colorMapSelect.disabled = true;
          colorMapSelect.style.opacity = "0.5";
          colorMapSelect.style.cursor = "not-allowed";
          return;
        }
        colorMapSelect.disabled = false;
        colorMapSelect.style.opacity = "1";
        colorMapSelect.style.cursor = "pointer";
        const maps = variable.type === "categorical" ? COLOR_MAPS.categorical : COLOR_MAPS.continuous;
        colorMapSelect.innerHTML = maps
          .map((map) => `<option value="${map.id}">${map.name}</option>`)
          .join("");
        if (!maps.find(m => m.id === state.colorMap)) {
          state.colorMap = maps[0].id;
        }
        colorMapSelect.value = state.colorMap;
      }

      function renderGridSelectors() {
        gridLayerSelect.innerHTML = GRID_LAYERS.map(
          (layer) => `<option value="${layer.id}">${layer.name}</option>`
        ).join("");
        gridLayerSelect.value = state.gridLayer;
        updateGridVariables();
      }

      function updateGridVariables() {
        const layer = GRID_LAYERS.find((item) => item.id === state.gridLayer);
        gridVariableSelect.innerHTML = layer.variables
          .map((variable) => `<option value="${variable.id}">${variable.label}</option>`)
          .join("");
        if (!layer.variables.find((item) => item.id === state.gridVariable)) {
          state.gridVariable = layer.variables[0].id;
        }
        gridVariableSelect.value = state.gridVariable;
        const variable = layer.variables.find((item) => item.id === state.gridVariable);
        if (variable) {
          const minText = formatLegendValue(variable.min);
          const maxText = formatLegendValue(variable.max);
          gridLegend.children[0].textContent = `Min ${minText}`;
          gridLegend.children[1].textContent = `Max ${maxText}`;
        } else {
          gridLegend.children[0].textContent = "Min —";
          gridLegend.children[1].textContent = "Max —";
        }
        renderGridOverlay();
      }

      function formatValue(value) {
        if (value === null || value === undefined || value === "") {
          return "—";
        }
        if (typeof value === "number") {
          const formatter = new Intl.NumberFormat("en-US", { maximumFractionDigits: Math.abs(value) < 1 ? 2 : 0 });
          return formatter.format(value);
        }
        return value;
      }

      function getFeatureTitle(feature, dataset) {
        const field = dataset.display?.title_field;
        return field ? feature.properties[field] ?? feature.properties.name ?? "Untitled" : feature.properties.name ?? "Untitled";
      }

      function getFeatureSubtitle(feature, dataset) {
        const fields = dataset.display?.subtitle_fields ?? [];
        const parts = fields
          .map((field) => feature.properties[field])
          .filter(Boolean)
          .join(" • ");
        return parts || feature.summary || "";
      }

      function getFeatureMeta(feature, dataset) {
        const metaField = dataset.display?.meta_field;
        if (!metaField) return "";
        const raw = feature.properties[metaField];
        if (raw === undefined || raw === null || raw === "") return "";
        const label = dataset.display.meta_label ? ` ${dataset.display.meta_label}` : "";
        return `${formatValue(raw)}${label}`;
      }

      function renderWeightsTable() {
        weightsTable.innerHTML = PTI_SCORES.map((score) => {
          const values = state.weights[score.id];
          return `
            <tr data-score="${score.id}">
              <td>${score.label}</td>
              <td><input type="number" step="0.1" min="-1" max="1" value="${values.need}" data-kind="need" /></td>
              <td><input type="number" step="0.1" min="-1" max="1" value="${values.opp}" data-kind="opp" /></td>
            </tr>
          `;
        }).join("");
      }

      function recomputeScores() {
        const need = Object.entries(state.weights).reduce((sum, [_, values], index) => sum + values.need * (0.1 * (index + 1)), 0);
        const opportunity = Object.entries(state.weights).reduce((sum, [_, values], index) => sum + values.opp * (0.08 * (index + 1)), 0);
        const combined = need + opportunity;
        scoreSummary.textContent = `Need: ${need.toFixed(2)} • Opportunity: ${opportunity.toFixed(2)} • Combined: ${combined.toFixed(2)}`;
      }

      function ensureMap() {
        if (map || typeof L === "undefined") {
          if (!map && typeof L === "undefined") {
            const fallback = document.createElement("div");
            fallback.id = "map-fallback";
            fallback.style.position = "absolute";
            fallback.style.inset = "0";
            fallback.style.display = "flex";
            fallback.style.alignItems = "center";
            fallback.style.justifyContent = "center";
            fallback.style.padding = "1rem";
            fallback.style.textAlign = "center";
            fallback.style.background = "rgba(7, 10, 22, 0.8)";
            fallback.textContent = "Leaflet failed to load. Check network access.";
            mapContainer.appendChild(fallback);
          }
          return;
        }
        map = L.map("map-root", {
          attributionControl: true,
          zoomControl: true,
        }).setView([15.5, 44], 6);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 18,
          attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);
        markersLayer = L.layerGroup().addTo(map);
      }

      function refreshMarkers(shouldFit = false) {
        ensureMap();
        if (!map || !markersLayer) return;
        markersLayer.clearLayers();
        if (!state.showSites) {
          renderGridOverlay();
          return;
        }
        const features = state.features;
        const variable = getActiveSiteVariable();
        const legendData = variable ? computeLegendData(features, variable, state.colorMap) : null;
        updateLegend(legendData, variable, state.colorMap);
        if (!features.length) {
          renderGridOverlay();
          return;
        }
        const latLngs = [];
        const baseSize = state.markerSize || 3;
        features.forEach((feature, index) => {
          const latLng = [feature.lat, feature.lon];
          latLngs.push(latLng);
          const value = variable ? getFeatureValue(feature, variable) : null;
          const color = colorForValue(value, legendData, state.colorMap);
          const isSelected = index === state.selectedIndex;
          const marker = L.circleMarker(latLng, {
            radius: isSelected ? baseSize + 3 : baseSize,
            color: isSelected ? "#ffffff" : color,
            weight: isSelected ? 2.5 : 1.5,
            fillColor: color,
            fillOpacity: 0.9,
          }).on("click", () => {
            state.selectedIndex = index;
            updatePanels();
            refreshMarkers();
          });
          const title = getFeatureTitle(feature, getActiveDataset());
          marker.bindTooltip(title, { direction: "top" });
          marker.addTo(markersLayer);
        });
        if (shouldFit && latLngs.length) {
          if (latLngs.length > 1) {
            map.fitBounds(latLngs, { padding: [30, 30] });
          } else {
            map.setView(latLngs[0], 10);
          }
        }
        renderGridOverlay();
      }

      function renderGridOverlay() {
        ensureMap();
        if (!map) return;
        if (gridOverlayLayer) {
          gridOverlayLayer.remove();
          gridOverlayLayer = null;
        }
        if (!state.showGrid) {
          updateGridLegendPanel(null, null, null);
          return;
        }
        const layerMeta = GRID_LAYERS.find((layer) => layer.id === state.gridLayer);
        if (!layerMeta) {
          updateGridLegendPanel(null, null, null);
          return;
        }
        const variable = layerMeta.variables.find((item) => item.id === state.gridVariable) ?? layerMeta.variables[0];
        if (!variable) {
          updateGridLegendPanel(null, layerMeta, null);
          return;
        }
        const valuesMap = GRID_VALUES[layerMeta.id] || {};
        const legendData = computeLegendDataFromGrid(valuesMap, variable, state.useLogScale);
        updateGridLegendPanel(legendData, layerMeta, variable);
        if (!legendData) {
          return;
        }
        gridOverlayLayer = L.geoJSON(GRID_GEOMETRY, {
          style: (feature) => {
            const h3 = feature?.properties?.h3_05;
            const row = valuesMap[h3] || {};
            const originalValue = row?.[variable.id] ?? null;
            // Store original value in feature properties for tooltip
            feature.properties._originalValue = originalValue;
            feature.properties._variableLabel = variable.label;
            // Transform for color calculation
            let value = originalValue;
            if (state.useLogScale && value !== null) {
              value = applyLogScale(value);
            }
            const color = colorForValue(value, legendData);
            return {
              color: "#1e293b",
              weight: 0.4,
              fillColor: color,
              fillOpacity: value === null ? 0 : 0.65,
            };
          },
        }).addTo(map);
        // Add tooltips to grid cells
        gridOverlayLayer.eachLayer((layer) => {
          if (layer.bringToBack) {
            layer.bringToBack();
          }
          const originalValue = layer.feature?.properties?._originalValue;
          const variableLabel = layer.feature?.properties?._variableLabel || variable.label;
          if (originalValue !== null && originalValue !== undefined) {
            const tooltipText = `${variableLabel}: ${formatValue(originalValue)}`;
            layer.bindTooltip(tooltipText, {
              permanent: false,
              direction: "center",
              className: "grid-tooltip",
            });
          }
        });
      }

      function updateDetailAttributes(container, fields, featureProperties) {
        container.innerHTML = "";
        if (!fields.length) {
          const empty = document.createElement("div");
          empty.className = "empty-state";
          empty.textContent = "No attributes configured.";
          container.appendChild(empty);
          return;
        }
        fields.forEach((field) => {
          const row = document.createElement("div");
          row.className = "kv";
          const label = document.createElement("span");
          label.className = "label";
          label.textContent = field.label;
          const value = document.createElement("span");
          value.textContent = formatValue(featureProperties[field.id]);
          row.appendChild(label);
          row.appendChild(value);
          container.appendChild(row);
        });
      }

      function updateGridContext(feature) {
        gridAttributesEl.innerHTML = "";
        const gridContext = feature.gridContext || {};
        if (!Object.keys(gridContext).length) {
          const empty = document.createElement("div");
          empty.className = "empty-state";
          empty.textContent = "No grid context available.";
          gridAttributesEl.appendChild(empty);
          return;
        }
        Object.entries(gridContext).forEach(([label, value]) => {
          const row = document.createElement("div");
          row.className = "kv";
          const labelEl = document.createElement("span");
          labelEl.className = "label";
          labelEl.textContent = label.split("_").join(" ");
          const valueEl = document.createElement("span");
          valueEl.textContent = value;
          row.appendChild(labelEl);
          row.appendChild(valueEl);
          gridAttributesEl.appendChild(row);
        });
      }

      function updatePanels() {
        const dataset = getActiveDataset();
        const variable = getActiveSiteVariable();
        const features = state.features;
        if (!features.length) {
          detailType.textContent = "Site";
          detailTitle.textContent = "No sample data";
          detailSubtitle.textContent = "Load a dataset to view site details.";
          siteAttributesEl.innerHTML = "";
          gridAttributesEl.innerHTML = "";
          return;
        }
        if (state.selectedIndex >= features.length) {
          state.selectedIndex = 0;
        }
        const feature = features[state.selectedIndex];
        const title = getFeatureTitle(feature, dataset);
        const subtitle = getFeatureSubtitle(feature, dataset);
        const fallbackSummary = feature.summary || "";

        detailType.textContent = dataset.label || "Site";
        detailTitle.textContent = title;
        detailSubtitle.textContent = subtitle || fallbackSummary;
        updateDetailAttributes(siteAttributesEl, dataset.detail_fields, feature.properties);
        updateGridContext(feature);
      }

      siteDatasetSelect.addEventListener("change", (event) => {
        state.siteDataset = event.target.value;
        state.features = SITE_FEATURES[state.siteDataset] || [];
        state.selectedIndex = 0;
        updateSiteVariables();
        updatePanels();
        markerSizeInput.value = state.markerSize;
        refreshMarkers(true);
      });

      siteVariableSelect.addEventListener("change", (event) => {
        state.siteVariable = event.target.value;
        updateSiteVariables();
        refreshMarkers();
      });

      if (colorMapSelect) {
        colorMapSelect.addEventListener("change", (event) => {
          state.colorMap = event.target.value;
          refreshMarkers();
        });
      }

      if (toggleSites) {
        toggleSites.addEventListener("change", () => {
          state.showSites = toggleSites.checked;
          refreshMarkers();
        });
      }

      if (markerSizeInput) {
        markerSizeInput.addEventListener("input", (event) => {
          const value = Math.max(1, Math.min(18, parseInt(event.target.value, 10) || 3));
          state.markerSize = value;
          if (markerSizeValue) {
            markerSizeValue.textContent = value;
          }
          refreshMarkers();
        });
      }

      gridLayerSelect.addEventListener("change", (event) => {
        state.gridLayer = event.target.value;
        updateGridVariables();
      });

      gridVariableSelect.addEventListener("change", (event) => {
        state.gridVariable = event.target.value;
        updateGridVariables();
      });

      if (toggleGrid) {
        toggleGrid.addEventListener("change", () => {
          state.showGrid = toggleGrid.checked;
          renderGridOverlay();
        });
      }

      if (toggleLogScale) {
        toggleLogScale.checked = state.useLogScale;
        toggleLogScale.addEventListener("change", () => {
          state.useLogScale = toggleLogScale.checked;
          renderGridOverlay();
        });
      }

      if (toggleNeed) {
        toggleNeed.addEventListener("change", () => {
          // Placeholder: need & opportunity layer rendering will respect this state in future iterations.
        });
      }

      tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
          tabButtons.forEach((item) => (item.dataset.active = "false"));
          button.dataset.active = "true";
          const tab = button.dataset.tab;
          if (tab === "map") {
            document.getElementById("map-container").style.display = "flex";
            document.getElementById("need-view").style.display = "none";
          } else {
            document.getElementById("map-container").style.display = "none";
            document.getElementById("need-view").style.display = "flex";
          }
        });
      });

      weightsTable.addEventListener("input", (event) => {
        if (event.target.tagName !== "INPUT") return;
        const row = event.target.closest("tr");
        const scoreId = row.dataset.score;
        const kind = event.target.dataset.kind;
        const value = Math.max(-1, Math.min(1, parseFloat(event.target.value) || 0));
        state.weights[scoreId][kind] = value;
      });

      document.getElementById("recompute-btn").addEventListener("click", recomputeScores);

      renderSiteSelectors();
      renderGridSelectors();
      renderWeightsTable();
      updateSiteVariables();
      updatePanels();
      refreshMarkers(true);
      recomputeScores();
    </script>
  </body>
</html>
    """

    html(
        template
        .replace("__SITE_DATASETS__", datasets_json)
        .replace("__SITE_FEATURES__", features_json)
        .replace("__GRID_DATASETS__", grid_datasets_json)
        .replace("__GRID_VALUES__", grid_values_json)
        .replace("__GRID_GEOMETRY__", grid_geometry_json),
        height=920,
        scrolling=False,
    )


