import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from docx import Document

from job_link_extractor import extract_job_text
from job_requirement_analyzer import extract_experience, extract_education, extract_responsibilities
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🚀", layout="wide")

st.title("🚀 Smart Resume Analyzer")
st.write("Upload your resume and paste a job link to analyze your job match.")

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


col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf","docx"])

with col2:
    job_url = st.text_input("Paste Job Description Link")


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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume Skills")
        st.write(resume_skills)

        st.subheader("Job Required Skills")
        st.write(job_skills)

    with col2:
        st.subheader("Matched Skills")
        st.write(list(matched))

        st.subheader("Missing Skills")
        st.write(list(missing))

    st.subheader("Resume Match Score")

    st.progress(int(score))
    st.success(f"{round(score,2)} % Match")

    labels = ["Matched Skills","Missing Skills"]
    values = [len(matched),len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels,values)

    st.pyplot(fig)

    st.subheader("Job Requirement Details")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.write("Experience")
        st.write(experience)

    with col2:
        st.write("Education")
        st.write(education)

    with col3:
        st.write("Responsibilities")
        st.write(responsibilities)

    st.subheader("Suggestions")

    if score < 50:
        st.warning("Your resume needs improvement. Add more relevant skills.")

    elif score < 75:
        st.info("Your resume is decent but could be improved by adding missing skills.")

    else:
        st.success("Great! Your resume matches the job very well.")
