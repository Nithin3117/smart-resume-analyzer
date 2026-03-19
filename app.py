import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from docx import Document
import plotly.graph_objects as go

from auth import login, signup, get_user, load_users, save_users
from job_link_extractor import extract_job_text
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.title("🔐 Login / Signup")

    option = st.selectbox("Choose Option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        if st.button("Signup"):
            success, msg = signup(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.stop()


# ---------------- THEME TOGGLE ----------------
def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp { background:#0f172a; color:white; }
        .card { background:#1e293b; padding:10px; border-radius:10px; margin:5px; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background:#f8fafc; color:black; }
        .card { background:#e2e8f0; padding:10px; border-radius:10px; margin:5px; }
        </style>
        """, unsafe_allow_html=True)


apply_theme()


# ---------------- SIDEBAR ----------------
username = st.session_state.username

st.sidebar.title("👤 Profile")
st.sidebar.write(f"Welcome, **{username}**")

if st.sidebar.button("🌗 Toggle Theme"):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


# ---------------- DISPLAY ----------------
def display_clean(title, items):
    st.markdown(f"### {title}")
    for item in items:
        st.markdown(f"<div class='card'>👉 {item}</div>", unsafe_allow_html=True)


# ---------------- RESUME READER ----------------
def extract_resume_text(file):
    text = ""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    else:
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text
    return text


# ---------------- SIMPLE EXTRACTION ----------------
def extract_info(text, keywords):
    return [l for l in text.lower().split("\n") if any(k in l for k in keywords)][:3]


# ---------------- SCORE ----------------
def calculate_score(resume_skills, job_skills):
    if not job_skills:
        return 0
    return (len(set(resume_skills) & set(job_skills)) / len(job_skills)) * 100


# ---------------- GAUGE ----------------
def show_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={'axis': {'range': [0, 100]}}
    ))
    st.plotly_chart(fig)


# ---------------- UI ----------------
st.title("🚀 Smart Resume Analyzer")

files = st.file_uploader("Upload Multiple Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_url = st.text_input("Paste Job Link")


# ---------------- MAIN ----------------
if files and job_url:

    job_text = extract_job_text(job_url)
    skills_list = load_skills("skills.txt")
    job_skills = extract_job_skills(job_text, skills_list)

    results = []

    for file in files:

        resume_text = extract_resume_text(file)
        tokens = preprocess(resume_text)
        resume_skills = extract_skills(tokens, skills_list)

        score = calculate_score(resume_skills, job_skills)
        missing = list(set(job_skills) - set(resume_skills))

        results.append((file.name, score, resume_skills, missing, resume_text))

    st.divider()

    for name, score, skills, missing, text in results:

        st.markdown(f"## 📄 {name}")

        display_clean("Experience", extract_info(text, ["intern", "experience"]))
        display_clean("Education", extract_info(text, ["btech", "degree"]))
        display_clean("Projects", extract_info(text, ["project"]))

        st.success("Skills: " + ", ".join(skills))
        st.error("Missing: " + ", ".join(missing))

        show_gauge(score)

        st.markdown("### 🤖 Suggestions")
        if missing:
            st.markdown(f"👉 Learn: {', '.join(missing)}")

        st.markdown("---")
