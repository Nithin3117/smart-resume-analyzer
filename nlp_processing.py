import re

# ---------- PREPROCESS ----------

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    return tokens


# ---------- EXTRACT SECTIONS ----------

def extract_sections(text):
    text = text.lower()

    education = []
    experience = []
    projects = []

    lines = text.split("\n")

    for line in lines:

        # EDUCATION
        if ("b.tech" in line or "degree" in line or "education" in line or "university" in line):
            education.append(line.strip())

        # EXPERIENCE
        elif ("experience" in line or "intern" in line or "worked" in line or "company" in line):
            experience.append(line.strip())

        # PROJECTS
        elif ("project" in line or "developed" in line or "built" in line):
            projects.append(line.strip())

    return education, experience, projects
