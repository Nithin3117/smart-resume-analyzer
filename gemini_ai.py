import google.generativeai as genai


# CONFIGURE GEMINI API
genai.configure(
    api_key="AIzaSyCNy-8WNnYS8WnT-y2pyeYed9NPdvsTt3A"
)

# LOAD MODEL
model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


# ---------- AI RESUME REVIEW ----------
def generate_ai_resume_review(
        resume_text,
        missing_skills,
        score
):

    resume_text = resume_text[:4000]

    prompt = f"""

    You are a professional ATS Resume Analyzer.

    Analyze this resume and provide:

    1. ATS improvement suggestions
    2. Missing important technical skills
    3. Resume enhancement ideas
    4. Better project descriptions
    5. Interview preparation tips

    ATS Score:
    {score}

    Missing Skills:
    {missing_skills}

    Resume:
    {resume_text}

    """

    response = model.generate_content(
        prompt
    )

    return response.text


# ---------- AI CHATBOT ----------
def ask_ai(question):

    prompt = f"""

    You are an AI Resume Assistant.

    Answer professionally.

    Question:
    {question}

    """

    response = model.generate_content(
        prompt
    )

    return response.text
