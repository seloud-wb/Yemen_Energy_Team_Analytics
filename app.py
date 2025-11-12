from typing import Any, Callable, Dict, cast
import os

import streamlit as st
from streamlit.components.v1 import html
from streamlit_navigation_bar import st_navbar

import pages as pg

# ------------------------------------------------------------
# Main Page Configuration
# ------------------------------------------------------------
# IMPORTANT: st.set_page_config() MUST be the first Streamlit command.
# This ensures proper session initialization, especially on Streamlit Cloud.
# Note: Streamlit automatically loads .streamlit/config.toml from the project root.
# No manual loading is required - the theme settings will be applied automatically.

st.set_page_config(initial_sidebar_state="collapsed", page_title="Yemen Energy Analytics Portal", layout="wide", page_icon=":earth_asia:")

# ------------------------------------------------------------
# Password Protection
# ------------------------------------------------------------
# Get password from environment variable or use default (for development)
# For production, set the APP_PASSWORD environment variable
APP_PASSWORD = os.getenv("APP_PASSWORD", "yemen2024")  # Change this default password

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# If not authenticated, show login form
if not st.session_state.authenticated:
    # Set page background to match app theme
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(99deg, #e9f5f3 67%, #fff 100%);
        }
        /* Hide navigation bar and menu on login page */
        header[data-testid="stHeader"],
        div[data-testid="stDecoration"],
        div[data-testid="stToolbar"],
        #MainMenu {
            display: none !important;
        }
        .stApp > header {
            display: none !important;
        }
        /* Hide Streamlit's default navigation */
        .stApp > div:first-child {
            padding-top: 0 !important;
        }
        .login-container {
            background: white;
            border-radius: 1.5rem;
            padding: 3rem 2.5rem;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
            border: 1px solid #e0e0e0;
            max-width: 500px;
            margin: 0 auto 1.5rem auto;
        }
        .login-logo {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .login-title {
            color: #125149;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .login-subtitle {
            color: #335250;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            width: 100%;
        }
        div[data-testid="stTextInput"] {
            max-width: 500px;
            margin: 0 auto;
        }
        div[data-testid="stTextInput"] > div > div {
            width: 100%;
        }
        div[data-testid="stTextInput"] label {
            color: #000000 !important;
            font-weight: 500;
        }
        div[data-testid="stButton"] {
            max-width: 500px;
            margin: 0 auto;
        }
        .stButton > button {
            background-color: #7fbbb4;
            color: white;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #5a9a94;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Center the login form
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Read logo file
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "wb_logo.svg")
    logo_svg = ""
    if os.path.exists(logo_path):
        with open(logo_path, "r", encoding="utf-8") as f:
            logo_svg = f.read()
    
    # Render login card with logo using html component
    html(
        f"""
        <style>
        .login-container {{
            background: white;
            border-radius: 1.5rem;
            padding: 3rem 2.5rem;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
            border: 1px solid #e0e0e0;
            max-width: 500px;
            margin: 0 auto 1.5rem auto;
        }}
        .login-logo {{
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
        }}
        .login-title {{
            color: #125149;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            margin-bottom: 0.5rem;
            text-align: center;
        }}
        </style>
        <div class="login-container">
            <div class="login-logo">
                {logo_svg if logo_svg else ""}
            </div>
            <h1 class="login-title">Yemen Energy Analytics Portal</h1>
        </div>
        """,
        height=250
    )
    
    # Password input - full width container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input(
            "Password",
            type="password",
            label_visibility="visible",
            key="password_input"
        )
        
        # Login button
        login_button = st.button("Login", type="primary", use_container_width=True)
        
        if login_button:
            if password_input == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.stop()  # Stop execution here if not authenticated

# ------------------------------------------------------------
# Navigation Configuration
# ------------------------------------------------------------
pages = ["Home", "YEEAP II Monitoring Dashboard", "RESET Geospatial Data Explorer"]
# Get absolute path to World Bank logo
logo_path = os.path.join(os.path.dirname(__file__), "assets", "wb_logo.svg")
logo_path = os.path.abspath(logo_path)

styles = {
    "nav": {
        "background-color": "rgb(127, 186, 180)",
        "height": "4rem",
        "padding": "0 2rem",
        "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
        "justify-content": "left",
    },
    "div": {
        "max-width": "50rem",
        "margin": "0 auto",
        "padding": "0 1rem",
    },
    "ul": {
        "gap": "0.5rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(8, 18, 17)",
        "padding": "0.625rem 1.25rem",
        "font-weight": "500",
        "font-size": "0.95rem",
        "transition": "all 0.2s ease",
        "white-space": "nowrap",
    },
    "img": {
        "height": "2.75rem",
        "margin-right": "1.5rem",
        "object-fit": "contain",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.3)",
        "font-weight": "600",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.4)",
    }
}
options = {"show_menu": True, "show_sidebar": False, "use_padding": True}

page = st_navbar(
    pages,
    styles=styles,
    options=cast(Any, options),
    logo_path=logo_path,
    logo_page="Home",  # Make logo clickable to navigate to Home
)

PAGES_MAP: Dict[str, Callable[[], None]] = {
    "Home": pg.home,
    "YEEAP II Monitoring Dashboard": pg.yeeap,
    "RESET Geospatial Data Explorer": pg.data_explorer,
}

PAGES_MAP.get(page, pg.home)()







