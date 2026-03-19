import streamlit as st
import time

# MUST FIRST
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

# IMPORTS
import PyPDF2
from docx import Document
import plotly.graph_objects as go

from auth import login, signup, reset_password
from email_utils import send_otp
from job_link_extractor import extract_job_text
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_time" not in st.session_state:
    st.session_state.otp_time = None


# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.logged_in:

    st.title("🔐 Secure Authentication")

    option = st.selectbox("Choose", ["Login", "Signup", "Forgot Password"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # SEND OTP FUNCTION
    def handle_send_otp():
        otp = send_otp(email)
        if otp:
            st.session_state.otp = otp
            st.session_state.otp_time = time.time()
            st.success("OTP sent to your email")
        else:
            st.error("Failed to send OTP")

    # ---------------- LOGIN ----------------
    if option == "Login":

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Send OTP"):
                handle_send_otp()

        with col2:
            if st.button("Resend OTP"):
                handle_send_otp()

        otp_input = st.text_input("Enter OTP")

        if st.button("Login"):
            if not st.session_state.otp:
                st.error("Please request OTP")

            elif time.time() - st.session_state.otp_time > 300:
                st.error("OTP expired")
                st.session_state.otp = None

            elif otp_input == st.session_state.otp:
                if login(email, password):
                    st.session_state.logged_in = True
                    st.session_state.username = email
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid password")

            else:
                st.error("Invalid OTP")

    # ---------------- SIGNUP ----------------
    elif option == "Signup":

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Send OTP"):
                handle_send_otp()

        with col2:
            if st.button("Resend OTP"):
                handle_send_otp()

        otp_input = st.text_input("Enter OTP")

        if st.button("Signup"):
            if otp_input == st.session_state.otp:
                success, msg = signup(email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.error("Invalid OTP")

    # ---------------- RESET ----------------
    else:

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Send OTP"):
                handle_send_otp()

        with col2:
            if st.button("Resend OTP"):
                handle_send_otp()

        otp_input = st.text_input("Enter OTP")
        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if otp_input == st.session_state.otp:
                success, msg = reset_password(email, new_password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.error("Invalid OTP")

    st.stop()


# ---------------- MAIN APP ----------------
st.title("🚀 Smart Resume Analyzer")

files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_url = st.text_input("Paste Job Link")


def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for p in reader.pages:
            text += p.extract_text()
    else:
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text
    return text


def calculate_score(resume_skills, job_skills):
    if not job_skills:
        return 0
    return (len(set(resume_skills) & set(job_skills)) / len(job_skills)) * 100


if files and job_url:

    job_text = extract_job_text(job_url)
    skills_list = load_skills("skills.txt")
    job_skills = extract_job_skills(job_text, skills_list)

    for file in files:

        st.markdown(f"## 📄 {file.name}")

        resume_text = extract_text(file)
        tokens = preprocess(resume_text)
        resume_skills = extract_skills(tokens, skills_list)

        score = calculate_score(resume_skills, job_skills)
        missing = list(set(job_skills) - set(resume_skills))

        st.success("Skills: " + ", ".join(resume_skills))
        st.error("Missing: " + ", ".join(missing))

        fig = go.Figure(go.Indicator(mode="gauge+number", value=score))
        st.plotly_chart(fig)

        st.markdown("### Suggestions")

        if missing:
            st.markdown(f"👉 Learn: {', '.join(missing)}")

        st.markdown("---")
