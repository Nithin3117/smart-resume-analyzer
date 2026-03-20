import streamlit as st
import PyPDF2
import docx
import plotly.graph_objects as go
import random
import requests

from auth import signup, login
from job_link_extractor import extract_job_text
from nlp_processing import preprocess, extract_sections
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match

# ---------- CONFIG ----------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

# ---------- SECRETS ----------
BREVO_API_KEY = st.secrets["BREVO_API_KEY"]
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = ""

# ---------- EMAIL FUNCTION ----------
def send_otp(email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Resume Analyzer",
            "email": SENDER_EMAIL
        },
        "to": [{"email": email}],
        "subject": "Your OTP Code",
        "htmlContent": f"<h2>Your OTP is: {otp}</h2>"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return True
    else:
        print("EMAIL ERROR:", response.text)
        return False


# ---------- FILE READERS ----------
def extract_text_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_text_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


# ---------- GAUGE ----------
def create_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "green"}
            ]
        }
    ))
    return fig


# ---------- LOGIN + OTP ----------
if not st.session_state.logged_in:

    st.title("🔐 Secure Login")

    option = st.selectbox("Choose", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):

        otp = str(random.randint(1000, 9999))

        success = send_otp(email, otp)

        if success:
            st.session_state.generated_otp = otp
            st.session_state.otp_sent = True
            st.success("OTP sent to your email ✅")
        else:
            st.session_state.otp_sent = False
            st.error("❌ Failed to send OTP. Check API / sender email")

    # ---------- OTP VERIFY ----------
    if st.session_state.otp_sent:

        st.subheader("Enter OTP")
        user_otp = st.text_input("OTP")

        if st.button("Verify OTP"):

            if user_otp == st.session_state.generated_otp:

                if option == "Signup":
                    success, msg = signup(email, password)
                else:
                    success, msg = login(email, password)

                if success:
                    st.session_state.logged_in = True
                    st.success("Login successful ✅")
                    st.rerun()
                else:
                    st.error(msg)

            else:
                st.error("Invalid OTP ❌")

# ---------- DASHBOARD ----------
else:

    st.title("🚀 Smart Resume Analyzer Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.otp_sent = False
        st.rerun()

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    job_url = st.text_input("Paste Job Link")

    job_text = ""
    if job_url:
        job_text = extract_job_text(job_url)

    if uploaded_file:

        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_pdf(uploaded_file)
        else:
            resume_text = extract_text_docx(uploaded_file)

        tokens = preprocess(resume_text)

        skills_list = load_skills("skills.txt")

        resume_skills = extract_skills(tokens, skills_list)
        job_skills = extract_job_skills(job_text, skills_list)

        score, matched, missing = calculate_match(resume_skills, job_skills)

        education, experience, projects = extract_sections(resume_text)

        # ---------- OUTPUT ----------
        st.plotly_chart(create_gauge(score))

        st.subheader("✅ Matched Skills")
        for s in matched:
            st.write(f"➡ {s}")

        st.subheader("❌ Missing Skills")
        for s in missing:
            st.write(f"➡ {s}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🎓 Education")
            for i in education:
                st.write(f"➡ {i}")

        with col2:
            st.markdown("### 💼 Experience")
            for i in experience:
                st.write(f"➡ {i}")

        with col3:
            st.markdown("### 🚀 Projects")
            for i in projects:
                st.write(f"➡ {i}")

        st.subheader("🤖 Suggestions")

        if missing:
            for s in missing:
                st.write(f"➡ Learn {s}")
