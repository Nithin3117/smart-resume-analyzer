import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from docx import Document

from job_link_extractor import extract_job_text
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#4CAF50;'>🚀 Smart Resume Analyzer</h1>
    <p style='text-align:center;'>Upload your resume and paste a job link to analyze how well you match the job requirements.</p>
    """,
    unsafe_allow_html=True
)

# ---------------- FUNCTION TO READ RESUME ----------------
def extract_text(file):

    text = ""

    # PDF support
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    # DOCX support
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text

    return text


# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

with col2:
    job_url = st.text_input("🔗 Paste Job Description Link")


# ---------------- MAIN LOGIC ----------------
if uploaded_file is not None and job_url != "":

    # Extract resume text
    resume_text = extract_text(uploaded_file)

    tokens = preprocess(resume_text)

    skills_list = load_skills("skills.txt")

    resume_skills = extract_skills(tokens, skills_list)

    # Extract job text from URL
    job_text = extract_job_text(job_url)

    job_skills = extract_job_skills(job_text, skills_list)

    score, matched, missing = calculate_match(resume_skills, job_skills)

    st.divider()

    # ---------------- RESULTS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Resume Skills Detected")
        st.write(resume_skills)

        st.subheader("📋 Job Required Skills")
        st.write(job_skills)

    with col2:
        st.subheader("✅ Matched Skills")
        st.write(list(matched))

        st.subheader("❌ Missing Skills")
        st.write(list(missing))


    # ---------------- MATCH SCORE ----------------
    st.subheader("🎯 Resume Match Score")

    st.progress(int(score))
    st.success(str(round(score, 2)) + "% Match")


    # ---------------- GRAPH ----------------
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)

    st.subheader("📊 Skill Match Graph")
    st.pyplot(fig)


    # ---------------- SUGGESTIONS ----------------
    st.subheader("💡 Suggestions")

    if score < 50:
        st.warning("Your resume needs improvement. Add more relevant skills.")

    elif score < 75:
        st.info("Your resume is decent but adding missing skills can improve it.")

    else:
        st.success("Great! Your resume matches the job very well.")
