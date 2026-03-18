import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import load_job_description, extract_job_skills, calculate_match


def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        text += page.extract_text()

    return text


st.title("🚀 Smart Resume Analyzer")
st.write("Upload your resume and check how well it matches the job requirements.")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if uploaded_file is not None:

    resume_text = extract_text(uploaded_file)

    tokens = preprocess(resume_text)

    skills_list = load_skills("skills.txt")

    resume_skills = extract_skills(tokens, skills_list)

    job_text = load_job_description("job_description.txt")

    job_skills = extract_job_skills(job_text, skills_list)

    score, matched, missing = calculate_match(resume_skills, job_skills)

    st.subheader("📌 Resume Skills Detected")
    st.write(resume_skills)

    st.subheader("📋 Job Required Skills")
    st.write(job_skills)

    st.subheader("✅ Matched Skills")
    st.write(list(matched))

    st.subheader("❌ Missing Skills")
    st.write(list(missing))

    st.subheader("🎯 Resume Match Score")
    st.success(str(round(score,2)) + "%")

    # -------- Graph --------
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.subheader("📊 Skill Match Graph")
    st.pyplot(fig)

    # -------- Suggestions --------
    if score < 50:
        st.warning("Your resume needs improvement. Add more relevant skills.")

    elif score < 75:
        st.info("Your resume is decent but adding missing skills can improve it.")

    else:
        st.success("Great! Your resume matches the job very well.")