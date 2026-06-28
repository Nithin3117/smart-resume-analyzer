import streamlit as st
import re
from resume_parser import extract_text_pdf, extract_text_docx
from charts import create_gauge
from job_link_extractor import extract_job_text
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match
from score_breakdown import calculate_breakdown
from ai_resume_improver import improve_resume
from job_recommender import recommend_jobs

# PAGE CONFIG

st.set_page_config(
    page_title="Smart Resume Analyzer",
    layout="wide"
)

# CUSTOM CSS

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

# PREPROCESS

def preprocess(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.split()

# EXTRACT RESUME SECTIONS

def extract_sections(text):
    text = text.replace("\t", "\n")
    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # SECTION HEADINGS
   
    section_keywords = {
        "education": [
            "education",
            "academic details",
            "academic background"
        ],
        
        "experience": [
            "experience",
            "work experience",
            "internship",
            "employment"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "certificates": [
            "certifications",
            "certificates",
            "achievement"
        ],

        "skills": [
            "skills",
            "technical skills",
            "tools",
            "technologies"
        ]
    }

    # STORAGE
   
    sections = {
        "education": [],
        "experience": [],
        "projects": [],
        "certificates": [],
        "skills": []
    }
    current_section = None

    # DETECT SECTIONS
  
    for line in lines:

        clean_line = line.lower().strip()

        found_new_section = False

        # CHECK SECTION TITLES

        for section, keywords in section_keywords.items():
            if clean_line in keywords:
                current_section = section
                found_new_section = True
                break

        # SKIP SECTION TITLES

        if found_new_section:
            continue

        # ADD CONTENT UNDER CURRENT SECTION

        if current_section:
            if len(line) > 3:
                cleaned_line = re.sub(
                    r'^[•●◦▪➤▶♦★✓✔➢➣\\-]+',
                    '',
                    line
                ).strip()
                cleaned_line = re.sub(
                    r'\\s+',
                    ' ',
                    cleaned_line
                )
                if cleaned_line:
                    sections[current_section].append(
                        cleaned_line
                    )

    # REMOVE DUPLICATES
  
    for key in sections:
        unique = []
        for item in sections[key]:
            if item not in unique:
                unique.append(item)
        sections[key] = unique
   
    # RETURN
   
    return (
        sections["education"],
        sections["experience"],
        sections["projects"],
        sections["certificates"],
        sections["skills"]
    )

# MAIN APP

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard",
        "About Project",
        "Tech Stack"
    ]
)

# DASHBOARD
if page == "Dashboard":

    st.title("Smart Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["pdf", "docx"]
    )

    job_url = st.text_input(
        "Job Description URL * "
    )

    job_text = ""

    if job_url:
        try:
            job_text = extract_job_text(job_url)
        except:
            st.warning("Unable to fetch job description.")
    if uploaded_file:
            
            # READ RESUME
        
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_pdf(uploaded_file)
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
            
            st.subheader("Resume Match Score")
            st.plotly_chart(
                create_gauge(score),
                use_container_width=True,
                config={"displayModeBar": False}
            )
            st.divider()

            # ATS BREAKDOWN
          
            st.subheader("ATS Resume Breakdown")
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
            
            st.subheader("Skills Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Matched Skills")
                if matched:
                    for skill in matched:
                        if skill.strip():
                            st.write(f"🔹 {skill}")
                else:
                    st.write("No matched skills")
            with col2:
                st.markdown("### Missing Skills")
                if missing:
                    for skill in missing:
                        if skill.strip():
                            st.write(f"🔹 {skill}")
                else:
                    st.write("No missing skills")
            st.divider()
          
            # CLEAN RESUME SUMMARY
           
            st.subheader("Resume Summary") 
    
            # 4 COLUMNS IN SINGLE ROW

            col1, col2, col3, col4 = st.columns(
                [1,1,1,1],
                gap="large"
            )

            # EDUCATION
          
            with col1:
                st.markdown("### Education")
                if education:

                    # SHOW TOP 3 EDUCATION DETAILS

                    for edu in education[:5]:
                        st.write(f"🔹 {edu}")
                else:
                    st.write("No education found")

            # SKILLS
            
            with col2:
                st.markdown("### Skills")
                if resume_skills:
                    top_skills = list(
                        set(resume_skills)
                    )[:5]
                    for skill in top_skills:
                        st.write(f"🔹 {skill}")
                else:
                    st.write("No skills found")

            # CERTIFICATES
           
            with col3:
                st.markdown("### Certificates")
                valid_certificates = []
                for cert in certificates:
                    cert_lower = cert.lower()
                    if (
                        "certificate" in cert_lower
                        or "certification" in cert_lower
                    ):
                        valid_certificates.append(cert)
                if valid_certificates:
                    for cert in valid_certificates[:3]:
                        st.write(f"🔹 {cert}")
                else:
                    st.write("No certificates found")

            # EXPERIENCE
           
            with col4:
                st.markdown("### Experience")
                if experience:
                    for exp in experience[:4]: 
                        st.write(f"🔹 {exp}")
                else:
                    st.write("No experience found")

            st.divider()

            st.subheader("Projects")

            if projects:

                st.markdown(f"### {projects[0]}")

                for desc in projects[1:]:

                    st.markdown(f"🔹 {desc}")

            else:

                st.write("No projects found")

            st.divider()
           
            # RECOMMENDED JOBS

            st.subheader("Recommended Jobs")
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
                "AI Resume Improvement Generator"
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

    # ABOUT PROJECT
    
    elif page == "About Project":
        st.title("About Project")
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

    # TECH STACK
    
    elif page == "Tech Stack":
        st.title("Technologies Used")
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
