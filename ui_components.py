import streamlit as st


# =====================================================
# OPEN CARD
# =====================================================

def open_card():

    st.markdown(
        """
        <div style="
            background-color:#1e1e2f;
            padding:20px;
            border-radius:18px;
            margin-bottom:20px;
            box-shadow:0px 4px 20px rgba(0,0,0,0.35);
        ">
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
            font-size:24px;
            font-weight:bold;
            margin-bottom:15px;
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
                <div style="
                    color:white;
                    font-size:17px;
                    margin-bottom:10px;
                    line-height:1.6;
                ">
                    🔹 {clean_item}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div style="
                color:#cccccc;
                font-size:16px;
            ">
                No data found
            </div>
            """,
            unsafe_allow_html=True
        )
