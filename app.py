import streamlit as st

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


# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "otp" not in st.session_state:
    st.session_state.otp = None


# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.logged_in:

    st.title("🔐 Authentication")

    option = st.selectbox("Choose", ["Login", "Signup", "Forgot Password"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # LOGIN
    if option == "Login":

        if st.button("Send OTP"):
            otp = send_otp(email)
            st.session_state.otp = otp
            st.success("OTP sent to email")
            st.info(f"Demo OTP: {otp}")  # 🔥 always visible

        otp_input = st.text_input("Enter OTP")

        if st.button("Login"):
            if otp_input == st.session_state.otp:
                if login(email, password):
                    st.session_state.logged_in = True
                    st.session_state.username = email
                    st.rerun()
                else:
                    st.error("Invalid password")
            else:
                st.error("Invalid OTP")

    # SIGNUP
    elif option == "Signup":

        if st.button("Send OTP"):
            otp = send_otp(email)
            st.session_state.otp = otp
            st.success("OTP sent")
            st.info(f"Demo OTP: {otp}")

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

    # RESET PASSWORD
    else:

        if st.button("Send OTP"):
            otp = send_otp(email)
            st.session_state.otp = otp
            st.success("OTP sent")
            st.info(f"Demo OTP: {otp}")

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


# ---------------- THEME ----------------
if st.session_state.theme == "dark":
    st.markdown("<style>.stApp{background:#0f172a;color:white}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp{background:#f8fafc;color:black}</style>", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.write(f"👤 {st.session_state.username}")

if st.sidebar.button("🌗 Toggle Theme"):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


# ---------------- APP ----------------
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
