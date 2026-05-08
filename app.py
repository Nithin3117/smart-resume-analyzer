import streamlit as st
import PyPDF2
import docx
import plotly.graph_objects as go

from auth import signup, login
from job_link_extractor import extract_job_text
from nlp_processing import preprocess, extract_sections
from skill_extractor import load_skills, extract_skills
from job_matcher import extract_job_skills, calculate_match


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")


# ---------- PREMIUM UI ----------
st.markdown("""
<style>

.main {
    background-color: #0f1117;
}

.card {
    background-color: #1e1e2f;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

.green {
    color: #00ff9f;
}

.red {
    color: #ff4b5c;
}

.blue {
    color: #4da6ff;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------- FILE READERS ----------
def extract_text_pdf(file):

    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def extract_text_docx(file):

    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# ---------- GAUGE ----------
def create_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",

        value=score,

        title={'text': "Resume Match Score"},

        gauge={

            'axis': {'range': [0, 100]},

            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "green"}
            ],

            'bar': {'color': "#00cc96"}
        }
    ))

    fig.update_layout(
        paper_bgcolor="#1e1e2f",
        font={'color': "white"}
    )

    return fig


# ---------- AI SUGGESTIONS ----------
def generate_ai_suggestions(resume_text, job_skills, missing_skills):

    suggestions = []

    if missing_skills:

        suggestions.append(
            f"Add important missing skills like {', '.join(missing_skills[:5])} to improve ATS score."
        )

    word_count = len(resume_text.split())

    if word_count < 150:

        suggestions.append(
            "Your resume is short. Add more detailed content about projects and skills."
        )

    elif word_count > 700:

        suggestions.append(
            "Your resume is too lengthy. Keep it concise."
        )

    if "project" not in resume_text.lower():

        suggestions.append(
            "Add strong projects with technologies and outcomes."
        )

    if "experience" not in resume_text.lower():

        suggestions.append(
            "Include internship or work experience."
        )

    suggestions.append(
        "Use job-specific keywords to improve ATS ranking."
    )

    suggestions.append(
        "Use strong action verbs like Developed, Built, Implemented."
    )

    return suggestions


# ================= LOGIN PAGE =================

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

    # ---------- SIGNUP ----------
    if option == "Signup":

        if st.button("Create Account"):

            success, msg = signup(email, password)

            if success:
                st.success(msg)

            else:
                st.error(msg)

    # ---------- LOGIN ----------
    else:

        if st.button("Login"):

            success, msg = login(email, password)

            if success:
                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:
                st.error(msg)


# ================= DASHBOARD =================

else:

    st.title("🚀 Smart Resume Analyzer Dashboard")

    # ---------- LOGOUT ----------
    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # ---------- INPUTS ----------
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

    # ---------- PROCESS ----------
    if uploaded_file:

        # Extract resume
        if uploaded_file.type == "application/pdf":

            resume_text = extract_text_pdf(uploaded_file)

        else:

            resume_text = extract_text_docx(uploaded_file)

        # NLP
        tokens = preprocess(resume_text)

        # Skills
        skills_list = load_skills("skills.txt")

        resume_skills = extract_skills(
            tokens,
            skills_list
        )

        job_skills = extract_job_skills(
            job_text,
            skills_list
        )

        # Match
        score, matched, missing = calculate_match(
            resume_skills,
            job_skills
        )

        # Sections
        education, experience, projects = extract_sections(
            resume_text
        )

        # ---------- SCORE ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.plotly_chart(
            create_gauge(score),
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------- SKILLS ----------
        col1, col2 = st.columns(2)

        with col1:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="title green">✅ Matched Skills</div>',
                unsafe_allow_html=True
            )

            if matched:

                for skill in matched:
                    st.markdown(f"➡ {skill.upper()}")

            else:
                st.write("No matched skills")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="title red">❌ Missing Skills</div>',
                unsafe_allow_html=True
            )

            if missing:

                for skill in missing:
                    st.markdown(f"➡ {skill.upper()}")

            else:
                st.success("No missing skills 🎉")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- DETAILS ----------
        st.markdown("## 📊 Resume Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="title blue">🎓 Education</div>',
                unsafe_allow_html=True
            )

            if education:

                for item in education:
                    st.markdown(f"➡ {item}")

            else:
                st.write("No education details found")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="title blue">💼 Experience</div>',
                unsafe_allow_html=True
            )

            if experience:

                for item in experience:
                    st.markdown(f"➡ {item}")

            else:
                st.write("No experience details found")

            st.markdown('</div>', unsafe_allow_html=True)

        with col3:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="title blue">🚀 Projects</div>',
                unsafe_allow_html=True
            )

            if projects:

                for item in projects:
                    st.markdown(f"➡ {item}")

            else:
                st.write("No project details found")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- AI ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            '<div class="title">🤖 AI Resume Suggestions</div>',
            unsafe_allow_html=True
        )

        ai_suggestions = generate_ai_suggestions(
            resume_text,
            job_skills,
            missing
        )

        for suggestion in ai_suggestions:
            st.markdown(f"➡ {suggestion}")

        st.markdown('</div>', unsafe_allow_html=True)
