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
        line = line.strip()

        if line == "":
            continue

        if len(line.split()) <= 2:
            continue  # remove useless words

        if "education" in line or "b.tech" in line or "degree" in line:
            education.append(line)

        elif "experience" in line or "intern" in line or "worked" in line:
            experience.append(line)

        elif "project" in line or "developed" in line or "built" in line:
            projects.append(line)

    return education, experience, projects
