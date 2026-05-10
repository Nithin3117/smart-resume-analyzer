import streamlit as st

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
# DASHBOARD PAGE
# =====================================================

def show_dashboard():

    st.title(
        "🚀 Smart Resume Analyzer Dashboard"
    )

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

        try:

            job_text = extract_job_text(
                job_url
            )

        except:

            st.warning(
                "Unable to extract job description from link."
            )

    # =====================================================
    # AFTER RESUME UPLOAD
    # =====================================================

    if uploaded_file:

        # =====================================================
        # READ RESUME
        # =====================================================

        try:

            if uploaded_file.type == "application/pdf":

                resume_text = extract_text_pdf(
                    uploaded_file
                )

            else:

                resume_text = extract_text_docx(
                    uploaded_file
                )

        except Exception as e:

            st.error(
                f"Resume reading failed: {e}"
            )

            return

        # =====================================================
        # CHECK RESUME TEXT
        # =====================================================

        if not resume_text.strip():

            st.error(
                "No text found in resume."
            )

            return

        # =====================================================
        # NLP PROCESSING
        # =====================================================

        tokens = preprocess(
            resume_text
        )

        # =====================================================
        # LOAD SKILLS
        # =====================================================

        skills_list = load_skills(
            "skills.txt"
        )

        # =====================================================
        # EXTRACT SKILLS
        # =====================================================

        resume_skills = extract_skills(
            tokens,
            skills_list
        )

        job_skills = extract_job_skills(
            job_text,
            skills_list
        )

        # =====================================================
        # SCORE
        # =====================================================

        score, matched, missing = calculate_match(
            resume_skills,
            job_skills
        )

        # =====================================================
        # EXTRACT RESUME SECTIONS
        # =====================================================

        try:

            education, experience, projects, certificates, skills = extract_sections(
                resume_text
            )

        except Exception as e:

            st.error(
                f"Section extraction failed: {e}"
            )

            education = []
            experience = []
            projects = []
            certificates = []
            skills = []

        # =====================================================
        # DEBUG OUTPUT
        # =====================================================

        st.write("### DEBUG INFO")

        st.write("Resume Text Preview:")
        st.write(resume_text[:1000])

        st.write("Education:", education)
        st.write("Experience:", experience)
        st.write("Projects:", projects)
        st.write("Certificates:", certificates)
        st.write("Skills:", skills)

        st.write("Matched Skills:", matched)
        st.write("Missing Skills:", missing)

        # =====================================================
        # BREAKDOWN
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
        # SCORE CARD
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

        # MATCHED SKILLS

        with col1:

            open_card()

            section_title(
                "✅ Matched Skills",
                "#00cc66"
            )

            display_list(
                matched
            )

            close_card()

        # MISSING SKILLS

        with col2:

            open_card()

            section_title(
                "❌ Missing Skills",
                "#ff4b5c"
            )

            display_list(
                missing
            )

            close_card()

        # =====================================================
        # RESUME DETAILS
        # =====================================================

        st.markdown(
            "## 📋 Resume Details"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        # EDUCATION

        with col1:

            open_card()

            section_title(
                "🎓 Education",
                "#4da6ff"
            )

            display_list(
                education
            )

            close_card()

        # EXPERIENCE

        with col2:

            open_card()

            section_title(
                "💼 Experience",
                "#ffaa00"
            )

            display_list(
                experience
            )

            close_card()

        # PROJECTS

        with col3:

            open_card()

            section_title(
                "🚀 Projects",
                "#b366ff"
            )

            display_list(
                projects
            )

            close_card()

        # CERTIFICATES

        with col4:

            open_card()

            section_title(
                "🏆 Certificates",
                "#ff66cc"
            )

            display_list(
                certificates
            )

            close_card()

        # SKILLS

        with col5:

            open_card()

            section_title(
                "🛠 Skills",
                "#00cc66"
            )

            display_list(
                skills
            )

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
                "No recommended jobs found"
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
