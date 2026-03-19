import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from docx import Document

from job_link_extractor import extract_job_text
from job_requirement_analyzer import extract_experience, extract_education, extract_responsibilities
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🚀", layout="wide")

st.title("🚀 Smart Resume Analyzer")
st.write("Upload your resume and paste a job link to analyze your job match.")


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


# ---------------- SCORE FUNCTION ----------------
def calculate_resume_score(resume_skills, job_skills, experience, education):

    if len(job_skills) == 0:
        skills_score = 0
    else:
        matched_skills = set(resume_skills).intersection(set(job_skills))
        skills_score = (len(matched_skills) / len(job_skills)) * 100

    exp_score = 50 if len(experience) > 0 else 20
    edu_score = 50 if len(education) > 0 else 20

    final_score = (0.6 * skills_score) + (0.2 * exp_score) + (0.2 * edu_score)

    return skills_score, exp_score, edu_score, final_score


# ---------------- AI SUGGESTIONS ----------------
def generate_ai_suggestions(missing_skills, score):

    suggestions = []

    if len(missing_skills) > 0:
        suggestions.append(
            "Learn and include these skills: " + ", ".join(missing_skills)
        )

    if score < 50:
        suggestions.append("Your resume is weak. Add more relevant projects and skills.")
        suggestions.append("Include internships or hands-on experience.")

    elif score < 75:
        suggestions.append("Your resume is decent. Add projects and certifications to improve.")
        suggestions.append("Highlight your achievements with measurable results.")

    else:
        suggestions.append("Your resume is strong. Focus on advanced projects and real-world impact.")

    suggestions.append("Add GitHub projects to showcase your work.")
    suggestions.append("Customize your resume for each job application.")

    return suggestions


# ---------------- INPUT UI ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    job_url = st.text_input("🔗 Paste Job Description Link")


# ---------------- MAIN LOGIC ----------------
if uploaded_file and job_url:

    resume_text = extract_resume_text(uploaded_file)

    tokens = preprocess(resume_text)

    skills_list = load_skills("skills.txt")

    resume_skills = extract_skills(tokens, skills_list)

    job_text = extract_job_text(job_url)

    job_skills = extract_job_skills(job_text, skills_list)

    score, matched, missing = calculate_match(resume_skills, job_skills)

    experience = extract_experience(job_text)
    education = extract_education(job_text)
    responsibilities = extract_responsibilities(job_text)

    skills_score, exp_score, edu_score, final_score = calculate_resume_score(
        resume_skills, job_skills, experience, education
    )

    ai_suggestions = generate_ai_suggestions(list(missing), final_score)

    st.divider()

    # -------- RESULTS --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Resume Skills")
        st.write(resume_skills)

        st.subheader("📋 Job Skills")
        st.write(job_skills)

    with col2:
        st.subheader("✅ Matched Skills")
        st.write(list(matched))

        st.subheader("❌ Missing Skills")
        st.write(list(missing))

    # -------- SCORE --------
    st.subheader("🎯 Resume Score Breakdown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Skills Match", f"{round(skills_score,2)}%")

    with col2:
        st.metric("Experience Match", f"{round(exp_score,2)}%")

    with col3:
        st.metric("Education Match", f"{round(edu_score,2)}%")

    st.subheader("🏆 Overall Resume Score")

    st.progress(int(final_score))
    st.success(f"{round(final_score,2)} % Match")

    # -------- GRAPH --------
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.subheader("📊 Skill Match Graph")
    st.pyplot(fig)

    # -------- JOB DETAILS --------
    st.subheader("📊 Job Requirement Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Experience")
        st.write(experience)

    with col2:
        st.write("Education")
        st.write(education)

    with col3:
        st.write("Responsibilities")
        st.write(responsibilities)

    # -------- AI SUGGESTIONS --------
    st.subheader("🤖 AI Suggestions")

    for suggestion in ai_suggestions:
        st.markdown(f"👉 {suggestion}")
