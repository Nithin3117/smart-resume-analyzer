import streamlit as st

from auth import signup, login
from chatbot import chatbot_response

from resume_parser import (
    extract_text_pdf,
    extract_text_docx
)

from charts import create_gauge

from ui_components import (
    open_card,
    close_card,
    section_title,
    display_list
)

from job_link_extractor import extract_job_text

from nlp_processing import (
    preprocess,
    extract_sections
)

from skill_extractor import (
    load_skills,
    extract_skills
)

from job_matcher import (
    extract_job_skills,
    calculate_match
)

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
# PREMIUM UI
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background-color: #0f1117;
}

.card {
    background-color: #1e1e2f;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
}

.title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
    background-color: #00cc66;
    color: white;
    border: none;
}

.stButton > button:hover {
    background-color: #00aa55;
    color: white;
}

a {
    color: #66ccff !important;
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    color: #00ffcc !important;
}

</style>
""", unsafe_allow_html=True)


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

    st.markdown("### Login / Signup")

    option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    # =====================================================
    # SIGNUP
    # =====================================================

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

    # =====================================================
    # LOGIN
    # =====================================================

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
# MAIN DASHBOARD
# =====================================================

else:

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("🤖 AI Resume Assistant")

    user_question = st.sidebar.text_input(
        "Ask something about your resume"
    )

    if user_question:

        answer = chatbot_response(
            user_question
        )

        st.sidebar.success(answer)

    st.sidebar.markdown("---")

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

        # =====================================================
        # LOGOUT
        # =====================================================

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.rerun()

        # =====================================================
        # INPUTS
        # =====================================================

        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf", "docx"]
        )

        job_url = st.text_input(
            "🌐 Paste Job Description Link"
        )

        job_text = ""

        if job_url:

            job_text = extract_job_text(
                job_url
            )

        # =====================================================
        # AFTER RESUME UPLOAD
        # =====================================================

        if uploaded_file:

            # =====================================================
            # READ RESUME
            # =====================================================

            if uploaded_file.type == "application/pdf":

                resume_text = extract_text_pdf(
                    uploaded_file
                )

            else:

                resume_text = extract_text_docx(
                    uploaded_file
                )

            # =====================================================
            # NLP PROCESSING
            # =====================================================

            tokens = preprocess(
                resume_text
            )

            # =====================================================
            # SKILLS EXTRACTION
            # =====================================================

            skills_list = load_skills(
                "skills.txt"
            )

            resume_skills = extract_skills(
                tokens,
                skills_list
            )

            job_skills = extract_job_skills(
                job_text,
                skills_list
            )

            # =====================================================
            # MATCH SCORE
            # =====================================================

            score, matched, missing = calculate_match(
                resume_skills,
                job_skills
            )

            # =====================================================
            # RESUME SECTIONS
            # =====================================================

            education, experience, projects, certificates, skills = extract_sections(
                resume_text
            )

            # =====================================================
            # ATS BREAKDOWN
            # =====================================================

            breakdown = calculate_breakdown(
                score,
                matched,
                missing,
                education,
                experience,
                projects
            )

            # =====================================================
            # RESUME SCORE CARD
            # =====================================================

            open_card()

            section_title(
                "📊 Resume Match Score"
            )

            st.plotly_chart(
                create_gauge(score),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            close_card()

            # =====================================================
            # ATS BREAKDOWN
            # =====================================================

            open_card()

            section_title(
                "📈 ATS Resume Breakdown"
            )

            cols = st.columns(
                len(breakdown)
            )

            for col, (key, value) in zip(
                cols,
                breakdown.items()
            ):

                with col:

                    st.metric(
                        label=key,
                        value=f"{value}%"
                    )

            close_card()

            # =====================================================
            # SKILLS ANALYSIS
            # =====================================================

            st.markdown(
                "## 🛠️ Skills Analysis"
            )

            col1, col2 = st.columns(2)

            # =====================================================
            # MATCHED SKILLS
            # =====================================================

            with col1:

                open_card()

                section_title(
                    "✅ Matched Skills",
                    "#00cc66"
                )

                display_list(matched)

                close_card()

            # =====================================================
            # MISSING SKILLS
            # =====================================================

            with col2:

                open_card()

                section_title(
                    "❌ Missing Skills",
                    "#ff4b5c"
                )

                display_list(missing)

                close_card()

            # =====================================================
            # RESUME DETAILS
            # =====================================================

            st.markdown(
                "## 📋 Resume Details"
            )

            col1, col2, col3, col4, col5 = st.columns(5)

            # =====================================================
            # EDUCATION
            # =====================================================

            with col1:

                open_card()

                section_title(
                    "🎓 Education",
                    "#4da6ff"
                )

                display_list(education)

                close_card()

            # =====================================================
            # EXPERIENCE
            # =====================================================

            with col2:

                open_card()

                section_title(
                    "💼 Experience",
                    "#ffaa00"
                )

                display_list(experience)

                close_card()

            # =====================================================
            # PROJECTS
            # =====================================================

            with col3:

                open_card()

                section_title(
                    "🚀 Projects",
                    "#b366ff"
                )

                display_list(projects)

                close_card()

            # =====================================================
            # CERTIFICATES
            # =====================================================

            with col4:

                open_card()

                section_title(
                    "🏆 Certificates",
                    "#ff66cc"
                )

                display_list(certificates)

                close_card()

            # =====================================================
            # SKILLS
            # =====================================================

            with col5:

                open_card()

                section_title(
                    "🛠 Skills",
                    "#00cc66"
                )

                display_list(skills)

                close_card()

            # =====================================================
            # RECOMMENDED JOBS
            # =====================================================

            open_card()

            section_title(
                "💼 Recommended Jobs"
            )

            recommended_jobs = recommend_jobs(
                resume_skills
            )

            if recommended_jobs:

                for job in recommended_jobs:

                    st.markdown(
                        f"🔹 [{job['title']}]({job['link']})"
                    )

            else:

                st.write(
                    "No jobs found"
                )

            close_card()

            # =====================================================
            # AI IMPROVEMENTS
            # =====================================================

            open_card()

            section_title(
                "✨ AI Resume Improvement Generator"
            )

            if st.button(
                "Generate Improvements"
            ):

                improvements = improve_resume(
                    missing,
                    education,
                    experience,
                    projects,
                    resume_text
                )

                display_list(
                    improvements
                )

            close_card()

    # =====================================================
    # ABOUT PROJECT
    # =====================================================

    elif page == "About Project":

        st.title(
            "📘 About Project"
        )

        st.markdown("""

## Smart Resume Analyzer

This project helps users:

- Analyze ATS compatibility
- Match skills with job descriptions
- Get AI-based resume improvements
- Discover recommended jobs
- Improve resume quality

### Features

✅ Resume Match Score  
✅ ATS Resume Breakdown  
✅ Skill Analysis  
✅ Resume Details  
✅ Recommended Jobs  
✅ AI Resume Improvement Generator  
✅ AI Chatbot Assistant  

""")

    # =====================================================
    # TECH STACK
    # =====================================================

    elif page == "Tech Stack":

        st.title(
            "🛠️ Technologies Used"
        )

        st.markdown("""

| Technology | Purpose |
|---|---|
| Python | Backend |
| Streamlit | Frontend |
| Plotly | Charts |
| NLP | Text Processing |
| HTML/CSS | UI Styling |

""")
