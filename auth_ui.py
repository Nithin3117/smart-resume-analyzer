import streamlit as st

from auth import signup, login


# =====================================================
# AUTH PAGE
# =====================================================

def show_auth_page():

    st.title(
        "🔐 Smart Resume Analyzer"
    )

    st.markdown(
        "### Login / Signup"
    )

    option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    email = st.text_input(
        "📧 Email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    # =====================================================
    # SIGNUP
    # =====================================================

    if option == "Signup":

        if st.button(
            "Create Account"
        ):

            success, msg = signup(
                email,
                password
            )

            if success:

                st.success(msg)

            else:

                st.error(msg)

    # =====================================================
    # LOGIN
    # =====================================================

    else:

        if st.button(
            "Login"
        ):

            success, msg = login(
                email,
                password
            )

            if success:

                st.session_state.logged_in = True

                st.success(
                    "Login Successful ✅"
                )

                st.rerun()

            else:

                st.error(msg)
