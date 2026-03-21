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


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

# ---------- PREMIUM UI CSS ----------
st.markdown("""
<style>
.card {
    background-color: #1e1e2f;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

.green {color: #00ff9f;}
.red {color: #ff4b5c;}
.blue {color: #4da6ff;}
</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = ""


# ---------- SECRETS ----------
BREVO_API_KEY = st.secrets["BREVO_API_KEY"]
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]


# ---------- EMAIL ----------
def send_otp(email, otp):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {"name": "Resume Analyzer", "email": SENDER_EMAIL},
        "to": [{"email": email}],
        "subject": "OTP Verification",
        "htmlContent": f"<h2>Your OTP is: {otp}</h2>"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 201


# ---------- FILE READERS ----------
def extract_text_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in reader.pages])


def extract_text_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


# ---------- GAUGE ----------
def create_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "green"}
            ]
        }
    ))
    return fig


# ================= LOGIN =================

if not st.session_state.logged_in:

    st.title("🔐 Secure Login")

    option = st.selectbox("Choose", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        otp = str(random.randint(1000, 9999))

        if send_otp(email, otp):
            st.session_state.generated_otp = otp
            st.session_state.otp_sent = True
            st.success("OTP sent to email ✅")
        else:
            st.error("Failed to send OTP ❌")

    if st.session_state.otp_sent:
        user_otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if user_otp == st.session_state.generated_otp:

                if option == "Signup":
                    success, msg = signup(email, password)
                else:
                    success, msg = login(email, password)

                if success:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Invalid OTP ❌")


# ================= DASHBOARD =================

else:

    st.title("🚀 Smart Resume Analyzer")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.otp_sent = False
        st.rerun()

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    job_url = st.text_input("Paste Job Link")

    job_text = extract_job_text(job_url) if job_url else ""

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

        # ---------- SCORE CARD ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(create_gauge(score), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- SKILLS CARDS ----------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="title green">✅ Matched Skills</div>', unsafe_allow_html=True)
            for s in matched:
                st.markdown(f"➡ {s.upper()}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="title red">❌ Missing Skills</div>', unsafe_allow_html=True)
            for s in missing:
                st.markdown(f"➡ {s.upper()}")
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- DETAILS ----------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="title blue">🎓 Education</div>', unsafe_allow_html=True)
            for i in education:
                st.markdown(f"➡ {i}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="title blue">💼 Experience</div>', unsafe_allow_html=True)
            for i in experience:
                st.markdown(f"➡ {i}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="title blue">🚀 Projects</div>', unsafe_allow_html=True)
            for i in projects:
                st.markdown(f"➡ {i}")
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- SUGGESTIONS ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="title">🤖 Suggestions</div>', unsafe_allow_html=True)

        if missing:
            for s in missing:
                st.markdown(f"➡ Learn {s}")
        else:
            st.success("Great profile! 🎉")

        st.markdown('</div>', unsafe_allow_html=True)
