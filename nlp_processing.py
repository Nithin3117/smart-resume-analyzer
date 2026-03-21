import re

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    return tokens


def extract_sections(text):
    text = text.lower()

    education = []
    experience = []
    projects = []

    lines = text.split("\n")

    current_section = None
    buffer = []

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        # Detect sections
        if "education" in line:
            current_section = "education"
            continue

        elif "experience" in line or "intern" in line:
            current_section = "experience"
            continue

        elif "project" in line:
            current_section = "projects"
            continue

        # Collect meaningful lines
        if current_section == "education":
            if len(line.split()) > 3:
                education.append(line)

        elif current_section == "experience":
            if len(line.split()) > 3:
                experience.append(line)

        elif current_section == "projects":
            if len(line.split()) > 3:
                projects.append(line)

    return education, experience, projects
