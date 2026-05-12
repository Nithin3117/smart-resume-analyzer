import streamlit as st

from resume_parser import (
    extract_text_pdf,
    extract_text_docx
)

from charts import create_gauge

from ui_components import (
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
# DASHBOARD
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
                "Unable to fetch job description."
            )

    # =====================================================
    # AFTER UPLOAD
    # =====================================================

    if uploaded_file:

        # =====================================================
        # EXTRACT RESUME TEXT
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
                f"Resume extraction failed: {e}"
            )

            return

        # =====================================================
        # CHECK EMPTY TEXT
        # =====================================================

        if not resume_text.strip():

            st.error(
                "No readable text found in resume."
            )

            return

        # =====================================================
        # NLP PROCESSING
        # =====================================================

        tokens = preprocess(
            resume_text
        )

        # =====================================================
        # SKILLS
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
        # EXTRACT SECTIONS
        # =====================================================

        education, experience, projects, certificates, skills = extract_sections(
            resume_text
        )

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
        # SCORE
        # =====================================================

        section_title(
            "📊 Resume Match Score",
            "#ffffff"
        )

        st.plotly_chart(
            create_gauge(score),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        st.divider()

        # =====================================================
        # ATS BREAKDOWN
        # =====================================================

        section_title(
            "📈 ATS Resume Breakdown",
            "#ffffff"
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
                    key,
                    f"{value}%"
                )

        st.divider()

        # =====================================================
        # SKILLS ANALYSIS
        # =====================================================

        section_title(
            "🛠 Skills Analysis",
            "#ffffff"
        )

        col1, col2 = st.columns(2)

        # MATCHED SKILLS

        with col1:

            section_title(
                "✅ Matched Skills",
                "#00cc66"
            )

            display_list(
                matched
            )

        # MISSING SKILLS

        with col2:

            section_title(
                "❌ Missing Skills",
                "#ff4b5c"
            )

            display_list(
                missing
            )

        st.divider()

        # =====================================================
        # RESUME DETAILS
        # =====================================================

        section_title(
            "📋 Resume Details",
            "#ffffff"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        # EDUCATION

        with col1:

            section_title(
                "🎓 Education",
                "#4da6ff"
            )

            display_list(
                education
            )

        # EXPERIENCE

        with col2:

            section_title(
                "💼 Experience",
                "#ffaa00"
            )

            display_list(
                experience
            )

        # PROJECTS

        with col3:

            section_title(
                "🚀 Projects",
                "#b366ff"
            )

            display_list(
                projects
            )

        # CERTIFICATES

        with col4:

            section_title(
                "🏆 Certificates",
                "#ff66cc"
            )

            display_list(
                certificates
            )

        # SKILLS

        with col5:

            section_title(
                "🛠 Skills",
                "#00cc66"
            )

            display_list(
                skills
            )

        st.divider()

        # =====================================================
        # RECOMMENDED JOBS
        # =====================================================

        section_title(
            "💼 Recommended Jobs",
            "#ffffff"
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

        st.divider()

        # =====================================================
        # AI IMPROVEMENTS
        # =====================================================

        section_title(
            "✨ AI Resume Improvement Generator",
            "#ffffff"
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
