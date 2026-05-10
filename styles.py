import streamlit as st


# =====================================================
# LOAD STYLES
# =====================================================

def load_styles():

    st.markdown("""
    <style>

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .main {
        background-color: #0f1117;
    }

    .card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
    }

    .title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-size: 16px;
        font-weight: bold;
        background-color: #00cc66;
        color: white;
        border: none;
    }

    .stButton > button:hover {
        background-color: #00aa55;
        color: white;
    }

    a {
        color: #66ccff !important;
        text-decoration: none;
        font-weight: bold;
    }

    a:hover {
        color: #00ffcc !important;
    }

    </style>
    """, unsafe_allow_html=True)
