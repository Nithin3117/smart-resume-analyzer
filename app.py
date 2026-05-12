import streamlit as st
import re

from auth import signup, login
from resume_parser import extract_text_pdf, extract_text_docx
from charts import create_gauge
from job_link_extractor import extract_job_text
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match
from score_breakdown import calculate_breakdown
from ai_resume_improver import improve_resume
from job_recommender import recommend_jobs


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00cc66;
        color: white;
        font-weight: bold;
        border: none;
    }

    .stButton > button:hover {
        background-color: #00aa55;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# PREPROCESS
# =====================================================

def preprocess(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.split()


# =====================================================
# EXTRACT RESUME SECTIONS
# =====================================================

def extract_sections(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:

        line = line.strip()

        if len(line) > 2:

            cleaned.append(line)

    education = []
    experience = []
    projects = []
    certificates = []
    skills = []

    for line in cleaned:

        lower = line.lower()

        # EDUCATION

        if any(word in lower for word in [
            "education",
            "college",
            "university",
            "b.tech",
            "cgpa"
        ]):

            education.append(line)

        # EXPERIENCE

        elif any(word in lower for word in [
            "experience",
            "internship",
            "work"
        ]):

            experience.append(line)

        # PROJECTS

        elif any(word in lower for word in [
            "project",
            "projects"
        ]):

            projects.append(line)

        # CERTIFICATES

        elif any(word in lower for word in [
            "certificate",
            "certification",
            "achievement"
        ]):

            certificates.append(line)

        # SKILLS

        elif any(word in lower for word in [
            "skills",
            "technical",
            "programming",
            "tools",
            "technologies"
        ]):

            skills.append(line)

    return (
        list(set(education)),
        list(set(experience)),
        list(set(projects)),
        list(set(certificates)),
        list(set(skills))
    )


# =====================================================
# SESSION
# =====================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 Smart Resume Analyzer")

    option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    # SIGNUP

    if option == "Signup":

        if st.button("Create Account"):

            success, msg = signup(
                email,
                password
            )

            if success:

                st.success(msg)

            else:

                st.error(msg)

    # LOGIN

    else:

        if st.button("Login"):

            success, msg = login(
                email,
                password
            )

            if success:

                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:

                st.error(msg)


# =====================================================
# MAIN APP
# =====================================================

else:

    st.sidebar.title("📌 Navigation")

    page = st.sidebar.radio(
        "Go To",
        [
            "Dashboard",
            "About Project",
            "Tech Stack"
        ]
    )

    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "Dashboard":

        st.title("🚀 Smart Resume Analyzer Dashboard")

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.rerun()

        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf", "docx"]
        )

        job_url = st.text_input(
            "🌐 Paste Job Description Link"
        )

        job_text = ""

        if job_url:

            try:

                job_text = extract_job_text(job_url)

            except:

                st.warning(
                    "Unable to fetch job description."
                )

        if uploaded_file:

            # READ RESUME

            if uploaded_file.type == "application/pdf":

                resume_text = extract_text_pdf(
                    uploaded_file
                )

            else:

                resume_text = extract_text_docx(
                    uploaded_file
                )

            if not resume_text.strip():

                st.error("No readable text found in resume")
                st.stop()

            # PROCESSING

            tokens = preprocess(resume_text)

            skills_list = load_skills("skills.txt")

            resume_skills = extract_skills(
                tokens,
                skills_list
            )

            job_skills = extract_job_skills(
                job_text,
                skills_list
            )

            score, matched, missing = calculate_match(
                resume_skills,
                job_skills
            )

            (
                education,
                experience,
                projects,
                certificates,
                skills
            ) = extract_sections(resume_text)

            breakdown = calculate_breakdown(
                score,
                matched,
                missing,
                education,
                experience,
                projects
            )

            # SCORE

            st.subheader("📊 Resume Match Score")

            st.plotly_chart(
                create_gauge(score),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            st.divider()

            # BREAKDOWN

            st.subheader("📈 ATS Resume Breakdown")

            cols = st.columns(len(breakdown))

            for col, (key, value) in zip(
                cols,
                breakdown.items()
            ):

                with col:

                    st.metric(
                        key,
                        f"{value}%"
                    )

            st.divider()

            # SKILLS ANALYSIS

            st.subheader("🛠 Skills Analysis")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### ✅ Matched Skills")

                if matched:

                    for skill in matched:

                        if skill.strip():

                            st.write(f"🔹 {skill}")

                else:

                    st.write("No matched skills")

            with col2:

                st.markdown("### ❌ Missing Skills")

                if missing:

                    for skill in missing:

                        if skill.strip():

                            st.write(f"🔹 {skill}")

                else:

                    st.write("No missing skills")

            st.divider()

            # RESUME DETAILS

            st.subheader("📋 Resume Details")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:

                st.markdown("### 🎓 Education")

                for item in education:

                    st.write(f"🔹 {item}")

            with col2:

                st.markdown("### 💼 Experience")

                for item in experience:

                    st.write(f"🔹 {item}")

            with col3:

                st.markdown("### 🚀 Projects")

                for item in projects:

                    st.write(f"🔹 {item}")

            with col4:

                st.markdown("### 🏆 Certificates")

                for item in certificates:

                    st.write(f"🔹 {item}")

            with col5:

                st.markdown("### 🛠 Skills")

                for item in skills:

                    st.write(f"🔹 {item}")

            st.divider()

            # JOBS

            st.subheader("💼 Recommended Jobs")

            recommended_jobs = recommend_jobs(
                resume_skills
            )

            if recommended_jobs:

                for job in recommended_jobs:

                    st.markdown(
                        f"🔹 [{job['title']}]({job['link']})"
                    )

            else:

                st.write("No jobs found")

            st.divider()

            # AI IMPROVEMENTS

            st.subheader(
                "✨ AI Resume Improvement Generator"
            )

            if st.button("Generate Improvements"):

                improvements = improve_resume(
                    missing,
                    education,
                    experience,
                    projects,
                    resume_text
                )

                if improvements:

                    for tip in improvements:

                        st.write(f"🔹 {tip}")

                else:

                    st.write(
                        "No suggestions available"
                    )

    # =====================================================
    # ABOUT PROJECT
    # =====================================================

    elif page == "About Project":

        st.title("📘 About Project")

        st.markdown(
            """
            ## Smart Resume Analyzer

            This project helps users:

            - Analyze ATS compatibility
            - Match resume skills with job descriptions
            - Get AI-based resume improvements
            - Discover recommended jobs
            - Improve resume quality
            """
        )

    # =====================================================
    # TECH STACK
    # =====================================================

    elif page == "Tech Stack":

        st.title("🛠 Technologies Used")

        st.markdown(
            """
            | Technology | Purpose |
            |---|---|
            | Python | Backend |
            | Streamlit | Frontend |
            | Plotly | Charts |
            | NLP | Text Processing |
            """
        )
