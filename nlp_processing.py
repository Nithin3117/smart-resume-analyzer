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

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        # Detect section headers
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
        if len(line.split()) > 3:
            if current_section == "education":
                education.append(line)

            elif current_section == "experience":
                experience.append(line)

            elif current_section == "projects":
                projects.append(line)

    return education, experience, projects
