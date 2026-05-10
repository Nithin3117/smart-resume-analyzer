import streamlit as st

from styles import load_styles

from auth_ui import (
    show_auth_page
)

from sidebar import (
    show_sidebar
)

from dashboard_ui import (
    show_dashboard
)

from pages import (
    show_about_page,
    show_tech_stack_page
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="wide"
)


# =====================================================
# LOAD STYLES
# =====================================================

load_styles()


# =====================================================
# SESSION
# =====================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    show_auth_page()


# =====================================================
# MAIN APP
# =====================================================

else:

    # =====================================================
    # SIDEBAR
    # =====================================================

    page = show_sidebar()

    # =====================================================
    # DASHBOARD PAGE
    # =====================================================

    if page == "Dashboard":

        show_dashboard()

    # =====================================================
    # ABOUT PAGE
    # =====================================================

    elif page == "About Project":

        show_about_page()

    # =====================================================
    # TECH STACK PAGE
    # =====================================================

    elif page == "Tech Stack":

        show_tech_stack_page()
