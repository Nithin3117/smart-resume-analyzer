import re


def preprocess(text):

    text = text.lower()

    tokens = re.findall(r'\b[a-z]+\b', text)

    return tokens


def extract_sections(text):

    lines = text.split("\n")

    education = []
    experience = []
    projects = []
    certificates = []

    current_section = None

    buffer = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # =====================================================
        # SECTION HEADINGS
        # =====================================================

        if "education" in lower:

            current_section = "education"
            continue

        elif "experience" in lower:

            current_section = "experience"
            continue

        elif "project" in lower:

            current_section = "projects"
            continue

        elif (
            "certificate" in lower or
            "certification" in lower
        ):

            current_section = "certificates"
            continue

        # =====================================================
        # MERGE SMALL BROKEN LINES
        # =====================================================

        if len(line.split()) <= 3:

            buffer += " " + line

        else:

            if buffer:
                line = buffer + " " + line
                buffer = ""

            # =====================================================
            # ADD TO SECTION
            # =====================================================

            if current_section == "education":

                education.append(line)

            elif current_section == "experience":

                experience.append(line)

            elif current_section == "projects":

                projects.append(line)

            elif current_section == "certificates":

                certificates.append(line)

    return education, experience, projects, certificates
