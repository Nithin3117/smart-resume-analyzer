import streamlit as st
import PyPDF2
import docx
import plotly.graph_objects as go

from auth import signup, login
from chatbot import chatbot_response

from job_link_extractor import extract_job_text
from nlp_processing import preprocess, extract_sections
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
# PREMIUM UI
# =====================================================

st.markdown("""
<style>

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

.green {
    color: #00cc66;
}

.red {
    color: #ff4b5c;
}

.blue {
    color: #4da6ff;
}

.orange {
    color: #ffaa00;
}

.purple {
    color: #b366ff;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
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

if "show_login" not in st.session_state:
    st.session_state.show_login = False


# =====================================================
# PDF READER
# =====================================================

def extract_text_pdf(file):

    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# =====================================================
# DOCX READER
# =====================================================

def extract_text_docx(file):

    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# =====================================================
# ATS GAUGE
# =====================================================

def create_gauge(score):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=score,

        number={
            'font': {
                'size': 70,
                'color': "white"
            }
        },

        title={
            'text': "Resume Match Score",
            'font': {
                'size': 32,
                'color': "white"
            }
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "white",
                'thickness': 0.25
            },

            'bgcolor': "#1e1e2f",

            'steps': [

                {
                    'range': [0, 40],
                    'color': "#ff4b5c"
                },

                {
                    'range': [40, 60],
                    'color': "#f7c948"
                },

                {
                    'range': [60, 85],
                    'color': "#66ff99"
                },

                {
                    'range': [85, 100],
                    'color': "#00cc66"
                }
            ]
        }
    ))

    fig.update_layout(

        paper_bgcolor="#1e1e2f",

        font={'color': "white"},

        height=500
    )

    return fig


# =====================================================
# LANDING PAGE
# =====================================================

if not st.session_state.logged_in and not st.session_state.show_login:

    st.markdown("""

    <style>

    .hero {
        text-align: center;
        padding-top: 50px;
        padding-bottom: 50px;
    }

    .hero-title {
        font-size: 60px;
        font-weight: bold;
        color: white;
    }

    .hero-subtitle {
        font-size: 24px;
        color: #bbbbbb;
        margin-top: 20px;
    }

    .feature-card {
        background-color: #1e1e2f;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
    }

    .feature-title {
        font-size: 22px;
        font-weight: bold;
        margin-top: 10px;
        color: white;
    }

    .feature-text {
        color: #cccccc;
        margin-top: 10px;
    }

    </style>

    """, unsafe_allow_html=True)

    # HERO
    st.markdown("""

    <div class="hero">

        <div class="hero-title">
            🚀 Smart Resume Analyzer
        </div>

        <div class="hero-subtitle">
            AI-Powered ATS Resume Evaluation Platform
        </div>

    </div>

    """, unsafe_allow_html=True)

    # FEATURES
    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""

        <div class="feature-card">

            <h1>📊</h1>

            <div class="feature-title">
                ATS Score Analysis
            </div>

            <div class="feature-text">
                Analyze resume ATS compatibility instantly.
            </div>

        </div>

        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""

        <div class="feature-card">

            <h1>💼</h1>

            <div class="feature-title">
                Job Recommendations
            </div>

            <div class="feature-text">
                Get smart job recommendations based on skills.
            </div>

        </div>

        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""

        <div class="feature-card">

            <h1>🤖</h1>

            <div class="feature-title">
                AI Resume Improvements
            </div>

            <div class="feature-text">
                Improve your resume using intelligent suggestions.
            </div>

        </div>

        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # BUTTON
    if st.button("🚀 Get Started"):

        st.session_state.show_login = True

        st.rerun()


# =====================================================
# LOGIN PAGE
# =====================================================

elif not st.session_state.logged_in:

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

    # SIGNUP
    if option == "Signup":

        if st.button("Create Account"):

            success, msg = signup(email, password)

            if success:
                st.success(msg)

            else:
                st.error(msg)

    # LOGIN
    else:

        if st.button("Login"):

            success, msg = login(email, password)

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

    # SIDEBAR
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
    # DASHBOARD PAGE
    # =====================================================

    if page == "Dashboard":

        st.title("🚀 Smart Resume Analyzer Dashboard")

        # LOGOUT
        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.show_login = False

            st.rerun()

        # INPUTS
        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf", "docx"]
        )

        job_url = st.text_input(
            "🌐 Paste Job Description Link"
        )

        job_text = ""

        if job_url:
            job_text = extract_job_text(job_url)

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

            # NLP
            tokens = preprocess(
                resume_text
            )

            # SKILLS
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

            # SCORE
            score, matched, missing = calculate_match(
                resume_skills,
                job_skills
            )

            # DETAILS
            education, experience, projects = extract_sections(
                resume_text
            )

            # BREAKDOWN
            breakdown = calculate_breakdown(
                score,
                matched,
                missing,
                education,
                experience,
                projects
            )

            # =====================================================
            # RESUME MATCH SCORE
            # =====================================================

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="title">📊 Resume Match Score</div>',
                unsafe_allow_html=True
            )

            st.plotly_chart(
                create_gauge(score),
                use_container_width=True,
                config={
                    'displayModeBar': False
                }
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # =====================================================
            # ATS BREAKDOWN
            # =====================================================

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="title">📈 ATS Resume Breakdown</div>',
                unsafe_allow_html=True
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

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # =====================================================
            # SKILLS
            # =====================================================

            st.markdown(
                "## 🛠️ Skills Analysis"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="title green">✅ Matched Skills</div>',
                    unsafe_allow_html=True
                )

                if matched:

                    for skill in matched:

                        st.markdown(
                            f"➡ {skill.upper()}"
                        )

                else:

                    st.write(
                        "No matched skills found"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="title red">❌ Missing Skills</div>',
                    unsafe_allow_html=True
                )

                if missing:

                    for skill in missing:

                        st.markdown(
                            f"➡ {skill.upper()}"
                        )

                else:

                    st.success(
                        "No missing skills 🎉"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # =====================================================
            # RESUME DETAILS
            # =====================================================

            st.markdown(
                "## 📋 Resume Details"
            )

            col1, col2, col3 = st.columns(3)

            # EDUCATION
            with col1:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="title blue">🎓 Education</div>',
                    unsafe_allow_html=True
                )

                if education:

                    for item in education:

                        st.markdown(
                            f"➡ {item}"
                        )

                else:

                    st.write(
                        "No education details found"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # EXPERIENCE
            with col2:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="title orange">💼 Experience</div>',
                    unsafe_allow_html=True
                )

                if experience:

                    for item in experience:

                        st.markdown(
                            f"➡ {item}"
                        )

                else:

                    st.write(
                        "No experience details found"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # PROJECTS
            with col3:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="title purple">🚀 Projects</div>',
                    unsafe_allow_html=True
                )

                if projects:

                    for item in projects:

                        st.markdown(
                            f"➡ {item}"
                        )

                else:

                    st.write(
                        "No project details found"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            # =====================================================
            # RECOMMENDED JOBS
            # =====================================================

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="title">💼 Recommended Jobs</div>',
                unsafe_allow_html=True
            )

            recommended_jobs = recommend_jobs(
                resume_skills
            )

            for job in recommended_jobs:

                st.markdown(
                    f"➡ [{job['title']}]({job['link']})"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # =====================================================
            # AI RESUME IMPROVER
            # =====================================================

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="title">✨ AI Resume Improvement Generator</div>',
                unsafe_allow_html=True
            )

            if st.button("Generate Improvements"):

                improvements = improve_resume(
                    missing,
                    education,
                    experience,
                    projects,
                    resume_text
                )

                for tip in improvements:

                    st.markdown(
                        f"➡ {tip}"
                    )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    # =====================================================
    # ABOUT PAGE
    # =====================================================

    elif page == "About Project":

        st.title("📘 About Project")

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
    # TECH STACK PAGE
    # =====================================================

    elif page == "Tech Stack":

        st.title("🛠️ Technologies Used")

        st.markdown("""

        | Technology | Purpose |
        |---|---|
        | Python | Backend |
        | Streamlit | Frontend |
        | Plotly | Charts |
        | NLP | Text Processing |
        | PyPDF2 | PDF Reading |
        | HTML/CSS | UI Styling |

        """)
