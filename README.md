# Smart Resume Analyzer

An intelligent **ATS (Applicant Tracking System) Resume Analyzer** built with **Python and Streamlit** that helps job seekers understand how well their resume matches a specific job description.

The application analyzes an uploaded resume, extracts relevant skills and sections, compares them with the requirements of a job description, calculates ATS and skill-match scores, identifies skill gaps, evaluates resume quality, and provides actionable improvement suggestions through an interactive dashboard.

---

## Overview

Applying for jobs often requires tailoring a resume for every position. The Smart Resume Analyzer simplifies this process by automatically comparing a resume with a job description and presenting the results in an easy-to-understand dashboard.

The application can:

- Analyze PDF and DOCX resumes
- Extract technical skills from resumes and job descriptions
- Calculate ATS compatibility scores
- Analyze individual ATS score components
- Identify matched and missing skills
- Analyze job responsibilities and preferred skills
- Detect important job-description keywords
- Identify missing job keywords
- Analyze resume quality and completeness
- Extract major resume sections
- Recommend suitable job roles
- Generate resume improvement suggestions
- Provide a final recommendation based on the overall ATS score

---

## Key Features

### 1. Resume Upload

Users can upload their resume in:

- PDF format
- DOCX format

The application extracts the text automatically and uses it for further analysis.

---

### 2. Job Description Analysis

Users can paste a complete job description into the application.

The system analyzes the job description to identify:

- Job level
- Required experience
- Responsibilities
- Preferred skills
- Important keywords
- Technical requirements

---

### 3. ATS Resume Match Score

The application calculates an overall ATS compatibility score based on multiple resume factors.

The score considers:

- Skills Match
- Resume Quality
- Project Strength
- Education Strength

The result is displayed through an interactive gauge and detailed score breakdown.

---

### 4. ATS Score Breakdown

The dashboard provides individual scores for:

- ATS Compatibility
- Skills Match
- Education Strength
- Experience Strength
- Project Strength

This helps users understand which areas of their resume are strong and which areas can be improved.

---

### 5. Job Description Intelligence

The application analyzes the job description and displays:

- Job Level
- Experience Required
- Keyword Match

It also extracts important keywords from the job description for comparison with the resume.

---

### 6. Job Keywords Analysis

The analyzer identifies important keywords from the job description and separates them into:

- Matched Job Keywords
- Missing Job Keywords

This helps users understand which terms from the job description are already represented in their resume.

---

### 7. Job Responsibilities Detection

The system automatically identifies responsibilities from the job description.

Examples include responsibilities related to:

- Development
- Backend applications
- API integration
- Database operations
- Testing
- Debugging
- Maintenance

---

### 8. Preferred Skills Analysis

The application detects skills mentioned under areas such as:

- Preferred
- Nice to have
- Plus
- Bonus

These skills are displayed separately so users can understand additional qualifications expected by the employer.

---

### 9. Skill Gap Analysis

The Skill Gap Analysis compares the skills found in the resume with the skills detected in the job description.

It provides:

- Required Skill Match
- Preferred Skill Match
- Overall Skill Match
- Skills You Have
- Skills You Are Missing

This gives users a clear view of the technical gaps they may need to address.

---

### 10. Priority Skills to Learn

Missing skills are prioritized and converted into practical learning recommendations.

For example:

> Learn and practice FastAPI through a small practical project.

This makes the analysis more actionable instead of only showing missing keywords.

---

### 11. Resume Quality Analysis

The application evaluates the overall structure and completeness of the resume.

It provides:

- Resume Quality Score
- Word Count
- Bullet Point Count

It also provides feedback when a resume appears too short, too long, or within a reasonable length.

---

### 12. Resume Strengths

The analyzer checks for important resume components and identifies strengths such as:

- Education
- Experience
- Projects
- Technical Skills
- Certifications
- Email
- Phone Number
- LinkedIn
- GitHub

This gives users a quick overview of the sections and information already present in their resume.

---

### 13. Areas to Improve

The application generates actionable suggestions based on the resume and job description.

Suggestions can include:

- Adding relevant missing skills
- Adding internship or practical experience
- Improving project descriptions
- Adding certifications
- Tailoring resume content to job-description keywords
- Using concise, action-oriented bullet points
- Adding measurable outcomes

---

### 14. Resume Section Check

The dashboard verifies the presence of important resume sections:

- Contact Information
- Education
- Experience
- Projects
- Skills
- Certifications
- LinkedIn
- GitHub

Each section is clearly marked as **Present** or **Missing**.

---

### 15. Resume Summary

The application extracts and presents a structured summary of the resume, including:

- Education
- Skills
- Certificates
- Experience

This allows users to quickly review the information detected from their uploaded resume.

---

### 16. Project Analysis

The application presents the user's major projects in a structured dashboard.

The current project showcase includes:

#### Smart Resume Analyzer

- Resume parsing and analysis
- Skill extraction
- ATS score calculation
- Job description matching
- Resume improvement suggestions

#### Library Management System

- Full-stack web application
- React frontend
- FastAPI backend
- SQLAlchemy
- SQLite
- REST APIs
- JWT authentication
- Book and student management
- Issue and return tracking
- Fine calculation
- Dashboard statistics

#### Page Pulse

- Web application analysis
- React frontend
- FastAPI backend
- API integration
- Responsive result presentation

---

### 17. Recommended Jobs

Based on the skills detected in the job description, the application recommends relevant roles such as:

- Python Developer
- React Developer
- Backend Developer
- SQL / Backend Developer
- Software Developer

The recommendations dynamically change according to the detected job requirements.

---

### 18. AI Resume Improvement Generator

The application includes an interactive improvement generator that presents personalized resume suggestions based on the resume analysis and job description.

Users can generate improvement recommendations directly from the dashboard.

---

### 19. Final Recommendation

At the end of the analysis, the application provides an overall recommendation based on the ATS score.

The result categorizes the resume alignment as:

- Strong match
- Reasonable match
- Low match

This gives users a simple final assessment of how closely their resume aligns with the selected job.

---

## ATS Scoring

The ATS score is calculated using a weighted combination of several resume factors.

The current scoring model uses:

| Factor | Weight |
|---|---:|
| Skills Match | 45% |
| Resume Quality | 20% |
| Project Strength | 20% |
| Education Strength | 15% |

The final score is capped at 100.

This approach gives greater importance to technical skill alignment while also considering resume quality, projects, and education.

---

## Skill Extraction

The application maintains a collection of commonly used technical skills and identifies them from both resumes and job descriptions.

Examples include:

- Python
- Java
- JavaScript
- C
- C++
- C#
- React
- FastAPI
- Flask
- Django
- Streamlit
- HTML
- CSS
- SQL
- MySQL
- SQLite
- PostgreSQL
- MongoDB
- SQLAlchemy
- REST API
- JWT
- Git
- GitHub
- Docker
- AWS
- Azure
- GCP
- Machine Learning
- Artificial Intelligence
- NLP
- Natural Language Processing
- Pandas
- NumPy
- Scikit-learn
- TensorFlow
- PyTorch

The skill extraction process also normalizes detected skills to reduce duplicate results.

---

## Resume Processing

### PDF Processing

PDF resumes are processed using `pypdf` to extract text from individual pages.

### DOCX Processing

DOCX resumes are processed using `python-docx`.

The application extracts:

- Paragraph content
- Table content

The extracted information is then normalized and analyzed.

---

## Application Workflow

```text
Upload Resume
      ↓
Extract Resume Text
      ↓
Paste Job Description
      ↓
Analyze Resume
      ↓
Extract Resume Skills
      ↓
Extract Job Requirements & Keywords
      ↓
Compare Resume With Job Description
      ↓
Calculate ATS Score
      ↓
Analyze Skill Gaps
      ↓
Analyze Resume Quality
      ↓
Generate Recommendations

##  Author

**Nithin Bollineni**

GitHub : https://github.com/Nithin3117

Live Website : http://localhost:8501/

