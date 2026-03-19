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


# ---------------- LOGIN PAGE ----------------
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
                st.success("Login successful")
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


# ---------------- MAIN APP ----------------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")


# ---------------- SIDEBAR PROFILE ----------------
username = st.session_state.username
user_data = get_user(username)

st.sidebar.title("👤 Profile")
st.sidebar.write(f"Welcome, **{username}**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# SHOW HISTORY
if "history" in user_data and user_data["history"]:
    st.sidebar.subheader("📊 History")
    for item in user_data["history"][-5:]:
        st.sidebar.write(f"Score: {round(item['score'],2)}%")


# ---------------- UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.card {
    background: #1e293b;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 Smart Resume Analyzer</h1>", unsafe_allow_html=True)


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
def extract_experience(text):
    return [l for l in text.lower().split("\n") if "intern" in l or "experience" in l][:3] or ["No experience found"]

def extract_education(text):
    return [l for l in text.lower().split("\n") if "btech" in l or "degree" in l][:3] or ["No education found"]

def extract_projects(text):
    return [l for l in text.lower().split("\n") if "project" in l][:3] or ["No projects found"]


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


# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

with col2:
    job_url = st.text_input("Paste Job Link")


# ---------------- MAIN LOGIC ----------------
if file and job_url:

    resume_text = extract_resume_text(file)
    tokens = preprocess(resume_text)

    skills_list = load_skills("skills.txt")
    resume_skills = extract_skills(tokens, skills_list)

    job_text = extract_job_text(job_url)
    job_skills = extract_job_skills(job_text, skills_list)

    score = calculate_score(resume_skills, job_skills)

    missing = list(set(job_skills) - set(resume_skills))

    exp = extract_experience(resume_text)
    edu = extract_education(resume_text)
    proj = extract_projects(resume_text)

    st.divider()

    display_clean("Experience", exp)
    display_clean("Education", edu)
    display_clean("Projects", proj)

    st.subheader("Skills")
    st.success(", ".join(resume_skills))

    st.subheader("Missing Skills")
    st.error(", ".join(missing))

    st.subheader("Score")
    show_gauge(score)

    st.subheader("AI Suggestions")

    if missing:
        st.markdown(f"👉 Learn: {', '.join(missing)}")

    st.markdown("👉 Add projects")
    st.markdown("👉 Customize resume")

    # SAVE HISTORY
    users = load_users()
    if username in users:
        users[username]["history"].append({
            "score": score
        })
        save_users(users)
