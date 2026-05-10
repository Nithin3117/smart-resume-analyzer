import streamlit as st


# =====================================================
# ABOUT PROJECT PAGE
# =====================================================

def show_about_page():

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
# TECH STACK PAGE
# =====================================================

def show_tech_stack_page():

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
