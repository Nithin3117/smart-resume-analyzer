import streamlit as st


# =====================================================
# OPEN CARD
# =====================================================

def open_card():

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )


# =====================================================
# CLOSE CARD
# =====================================================

def close_card():

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =====================================================
# SECTION TITLE
# =====================================================

def section_title(title, color="white"):

    st.markdown(
        f'<div class="title" style="color:{color};">{title}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    return (
        text
        .replace("•", "")
        .replace("-", "")
        .strip()
    )


# =====================================================
# DISPLAY LIST
# =====================================================

def display_list(items):

    if items:

        for item in items:

            clean_item = clean_text(item)

            st.markdown(
                f"🔹 {clean_item}"
            )

    else:

        st.write("No data found")
