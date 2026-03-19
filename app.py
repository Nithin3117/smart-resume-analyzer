import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from docx import Document
import plotly.graph_objects as go

from job_link_extractor import extract_job_text
from job_requirement_analyzer import extract_experience, extract_education, extract_responsibilities
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🚀", layout="wide")


# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
h1 {
    text-align: center;
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<h1>🚀 Smart Resume Analyzer</h1>
<p style='text-align:center;'>AI-powered resume analysis system</p>
""", unsafe_allow_html=True)


# ---------------- RESUME READER ----------------
def extract_resume_text(file):
    text = ""

    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text

    return text


# ---------------- SCORE ----------------
def calculate_resume_score(resume_skills, job_skills, experience, education):

    if len(job_skills) == 0:
        skills_score = 0
    else:
        skills_score = (len(set(resume_skills) & set(job_skills)) / len(job_skills)) * 100

    exp_score = 50 if experience else 20
    edu_score = 50 if education else 20

    final_score = (0.6 * skills_score) + (0.2 * exp_score) + (0.2 * edu_score)

    return skills_score, exp_score, edu_score, final_score


# ---------------- GAUGE ----------------
def show_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Resume Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "lightgreen"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig)


# ---------------- REPORT ----------------
def generate_report(resume_skills, job_skills, matched, missing, score):
    return f"""
SMART RESUME ANALYSIS REPORT

Resume Skills:
{', '.join(resume_skills)}

Job Skills:
{', '.join(job_skills)}

Matched Skills:
{', '.join(matched)}

Missing Skills:
{', '.join(missing)}

Final Score:
{round(score,2)}%
"""


# ---------------- AI SUGGESTIONS (NO API) ----------------
def generate_ai_response(resume_skills, missing_skills, score):

    suggestions = []

    if missing_skills:
        suggestions.append("You are missing important skills: " + ", ".join(missing_skills))

    if score < 50:
        suggestions.append("Your resume is weak. Add more projects and technical skills.")
        suggestions.append("Include internships or real-world experience.")

    elif score < 75:
        suggestions.append("Your resume is good but can be improved.")
        suggestions.append("Add certifications and highlight achievements.")

    else:
        suggestions.append("Excellent resume! Focus on advanced topics.")

    suggestions.append("Add GitHub projects to showcase your work.")
    suggestions.append("Customize your resume for each job role.")

    return suggestions


# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

with col2:
    job_url = st.text_input("🔗 Paste Job Link")


# ---------------- MAIN ----------------
if uploaded_file and job_url:

    with st.spinner("🔍 Analyzing Resume..."):

        resume_text = extract_resume_text(uploaded_file)
        tokens = preprocess(resume_text)

        skills_list = load_skills("skills.txt")

        resume_skills = extract_skills(tokens, skills_list)

        job_text = extract_job_text(job_url)
        job_skills = extract_job_skills(job_text, skills_list)

        score, matched, missing = calculate_match(resume_skills, job_skills)

        experience = extract_experience(job_text)
        education = extract_education(job_text)

        skills_score, exp_score, edu_score, final_score = calculate_resume_score(
            resume_skills, job_skills, experience, education
        )

        ai_suggestions = generate_ai_response(resume_skills, list(missing), final_score)

    st.divider()

    # RESULTS
    col1, col2 = st.columns(2)

    col1.subheader("📌 Resume Skills")
    col1.success(", ".join(resume_skills))

    col2.subheader("❌ Missing Skills")
    col2.error(", ".join(missing))

    # SCORE
    st.subheader("🎯 Resume Score")
    show_gauge(final_score)

    # METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Skills", f"{round(skills_score,2)}%")
    col2.metric("Experience", f"{round(exp_score,2)}%")
    col3.metric("Education", f"{round(edu_score,2)}%")

    # GRAPH
    fig, ax = plt.subplots()
    ax.bar(["Matched", "Missing"], [len(matched), len(missing)])
    st.pyplot(fig)

    # DOWNLOAD REPORT
    report = generate_report(resume_skills, job_skills, matched, missing, final_score)

    st.download_button("📄 Download Report", report, "resume_report.txt")

    # AI SUGGESTIONS
    st.subheader("🤖 AI Suggestions")

    for s in ai_suggestions:
        st.info(s)


# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<p style='text-align:center;'>Built with ❤️ using Python & AI</p>
""", unsafe_allow_html=True)
