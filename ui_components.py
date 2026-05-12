import streamlit as st


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
        str(text)
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

            if clean_item:

                st.markdown(
                    f"🔹 {clean_item}"
                )

    else:

        st.write(
            "No data found"
        )
