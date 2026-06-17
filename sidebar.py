import streamlit as st

# SIDEBAR

def show_sidebar():
    st.sidebar.title(
        "Navigation"
    )
    page = st.sidebar.radio(
        "Go To",
        [
            "Dashboard",
            "About Project",
            "Tech Stack"
        ]
    )
    return page
