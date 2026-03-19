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


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1 {
    text-align: center;
    color: #38bdf8;
    font-size: 3rem;
}

.stButton>button {
    background-color: #38bdf8;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

[data-testid="stMetric"] {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<h1>🚀 Smart Resume Analyzer</h1>
<p style='text-align:center;'>Analyze your resume with AI & match it with real job roles</p>
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
        suggestions.append("Learn these skills: " + ", ".join(missing_skills))

    if score < 50:
        suggestions.append("Your resume is weak. Add more projects and skills.")
        suggestions.append("Include internships or hands-on experience.")

    elif score < 75:
        suggestions.append("Improve by adding certifications and projects.")
        suggestions.append("Highlight achievements with measurable results.")

    else:
        suggestions.append("Great resume! Focus on advanced skills.")

    suggestions.append("Add GitHub projects.")
    suggestions.append("Customize resume for each job.")

    return suggestions


# ---------------- INPUT UI ----------------
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

    with col2:
        job_url = st.text_input("🔗 Paste Job Link")


# ---------------- MAIN LOGIC ----------------
if uploaded_file and job_url:

    with st.spinner("🔍 Analyzing Resume... Please wait"):

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
        st.markdown("### 📌 Resume Skills")
        st.success(", ".join(resume_skills))

        st.markdown("### 📋 Job Skills")
        st.info(", ".join(job_skills))

    with col2:
        st.markdown("### ✅ Matched Skills")
        st.success(", ".join(matched))

        st.markdown("### ❌ Missing Skills")
        st.error(", ".join(missing))

    # -------- SCORE --------
    st.markdown("## 🏆 Overall Resume Score")

    st.progress(int(final_score))

    st.markdown(
        f"<h2 style='text-align:center; color:#22c55e;'>{round(final_score,2)}%</h2>",
        unsafe_allow_html=True
    )

    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)

    col1.metric("Skills Match", f"{round(skills_score,2)}%")
    col2.metric("Experience", f"{round(exp_score,2)}%")
    col3.metric("Education", f"{round(edu_score,2)}%")

    # -------- GRAPH --------
    labels = ["Matched", "Missing"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.subheader("📊 Skill Match Graph")
    st.pyplot(fig)

    # -------- JOB DETAILS --------
    st.subheader("📊 Job Details")

    col1, col2, col3 = st.columns(3)

    col1.write("Experience")
    col1.write(experience)

    col2.write("Education")
    col2.write(education)

    col3.write("Responsibilities")
    col3.write(responsibilities)

    # -------- AI SUGGESTIONS --------
    st.markdown("### 🤖 AI Suggestions")

    for suggestion in ai_suggestions:
        st.info(suggestion)

# -------- FOOTER --------
st.markdown("""
<hr>
<p style='text-align:center;'>Built with ❤️ using Python & AI</p>
""", unsafe_allow_html=True)
