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
    skills = []

    current_section = None

    current_project = ""

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
            "certification" in lower or
            "achievement" in lower
        ):

            current_section = "certificates"
            continue

        elif (
            "skill" in lower or
            "technical skill" in lower
        ):

            current_section = "skills"
            continue

        # =====================================================
        # EDUCATION
        # =====================================================

        if current_section == "education":

            education.append(line)

        # =====================================================
        # EXPERIENCE
        # =====================================================

        elif current_section == "experience":

            experience.append(line)

        # =====================================================
        # PROJECTS
        # =====================================================

        elif current_section == "projects":

            # MAIN PROJECT TITLE
            if (
                "resume analyzer" in lower or
                "project" in lower or
                "(" in line
            ):

                current_project = line

            else:

                if current_project:

                    current_project += "\n• " + line

            if current_project not in projects:

                projects.append(current_project)

        # =====================================================
        # CERTIFICATES
        # =====================================================

        elif current_section == "certificates":

            certificates.append(line)

        # =====================================================
        # SKILLS
        # =====================================================

        elif current_section == "skills":

            skills.append(line)

    return (
        education,
        experience,
        projects,
        certificates,
        skills
    )
