import streamlit as st
import PyPDF2
import docx
import plotly.graph_objects as go

from job_link_extractor import extract_job_text
from nlp_processing import preprocess, extract_sections
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


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


# ---------- AI SUGGESTIONS ----------

def generate_ai_response(resume_text, job_text, missing_skills):
    suggestions = []

    if len(missing_skills) > 0:
        suggestions.append("Add missing skills to match the job requirements")

    if "project" not in resume_text.lower():
        suggestions.append("Add more projects to strengthen your resume")

    if "experience" not in resume_text.lower():
        suggestions.append("Include internship or work experience")

    if len(resume_text.split()) < 200:
        suggestions.append("Increase resume content with more details")

    if "github" not in resume_text.lower():
        suggestions.append("Add GitHub or portfolio links")

    return suggestions


# ---------- GAUGE FUNCTION ----------

def create_gauge(score):
    color = "red"
    if score > 50:
        color = "orange"
    if score > 75:
        color = "green"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Resume Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},

            'steps': [
                {'range': [0, 50], 'color': "#ff4d4d"},
                {'range': [50, 75], 'color': "#ffa500"},
                {'range': [75, 100], 'color': "#00cc44"}
            ],
        }
    ))

    return fig


# ---------- UI ----------

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

st.title("🚀 Smart Resume Analyzer")
st.write("Upload your resume and compare with job requirements")

uploaded_file = st.file_uploader("Upload Resume (PDF / DOCX)", type=["pdf", "docx"])
job_url = st.text_input("Paste Job Description Link")

job_text = ""

if job_url:
    job_text = extract_job_text(job_url)


# ---------- MAIN LOGIC ----------

if uploaded_file is not None:

    # Read file
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_pdf(uploaded_file)
    else:
        resume_text = extract_text_docx(uploaded_file)

    # NLP
    tokens = preprocess(resume_text)

    # Skills
    skills_list = load_skills("skills.txt")
    resume_skills = extract_skills(tokens, skills_list)
    job_skills = extract_job_skills(job_text, skills_list)

    # Match
    score, matched, missing = calculate_match(resume_skills, job_skills)

    # Sections
    education, experience, projects = extract_sections(resume_text)

    # ---------- DISPLAY ----------

    st.subheader("📌 Resume Skills")
    st.success(", ".join(resume_skills))

    st.subheader("📋 Job Required Skills")
    st.info(", ".join(job_skills))

    st.subheader("✅ Matched Skills")
    for skill in matched:
        st.write(f"➡ {skill}")

    st.subheader("❌ Missing Skills")
    if missing:
        for skill in missing:
            st.write(f"➡ {skill}")
    else:
        st.write("🎉 No missing skills")

    # ---------- GAUGE SCORE ----------

    st.subheader("🎯 Resume Score")

    gauge_fig = create_gauge(score)
    st.plotly_chart(gauge_fig, use_container_width=True)

    # ---------- SECTIONS ----------

    st.subheader("📊 Resume Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎓 Education")
        if education:
            for item in education:
                st.write(f"➡ {item}")
        else:
            st.write("➡ No education details found")

    with col2:
        st.markdown("### 💼 Experience")
        if experience:
            for item in experience:
                st.write(f"➡ {item}")
        else:
            st.write("➡ No experience details found")

    with col3:
        st.markdown("### 🚀 Projects")
        if projects:
            for item in projects:
                st.write(f"➡ {item}")
        else:
            st.write("➡ No project details found")

    # ---------- AI SUGGESTIONS ----------

    ai_suggestions = generate_ai_response(resume_text, job_text, missing)

    st.subheader("🤖 AI Suggestions")

    for s in ai_suggestions:
        st.write(f"➡ {s}")

    # ---------- FINAL MESSAGE ----------

    if score < 50:
        st.error("Your resume needs improvement")
    elif score < 75:
        st.warning("Your resume is good but can improve")
    else:
        st.success("Excellent match! 🎉")
