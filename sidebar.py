import streamlit as st

from chatbot import chatbot_response


# =====================================================
# SIDEBAR
# =====================================================

def show_sidebar():

    st.sidebar.title(
        "🤖 AI Resume Assistant"
    )

    user_question = st.sidebar.text_input(
        "Ask something about your resume"
    )

    if user_question:

        answer = chatbot_response(
            user_question
        )

        st.sidebar.success(
            answer
        )

    st.sidebar.markdown("---")

    st.sidebar.title(
        "📌 Navigation"
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
