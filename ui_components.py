import streamlit as st


# =====================================================
# OPEN CARD
# =====================================================

def open_card():

    st.markdown(
        """
        <div class="card">
        """,
        unsafe_allow_html=True
    )


# =====================================================
# CLOSE CARD
# =====================================================

def close_card():

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# SECTION TITLE
# =====================================================

def section_title(title, color="#ffffff"):

    st.markdown(
        f"""
        <h3 style="
            color:{color};
            font-weight:bold;
            margin-bottom:15px;
            font-size:26px;
        ">
            {title}
        </h3>
        """,
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
                f"""
                <p style="
                    font-size:18px;
                    margin-bottom:10px;
                    color:white;
                ">
                    🔹 {clean_item}
                </p>
                """,
                unsafe_allow_html=True
            )

    else:

        st.write(
            "No data found"
        )
