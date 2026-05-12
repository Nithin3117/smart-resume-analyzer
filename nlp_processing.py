import re


# =====================================================
# PREPROCESS TEXT
# =====================================================

def preprocess(text):

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Simple tokenization
    tokens = text.split()

    return tokens


# =====================================================
# CLEAN LINES
# =====================================================

def clean_lines(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:

        line = line.strip()

        if len(line) > 2:

            cleaned.append(line)

    return cleaned


# =====================================================
# REMOVE DUPLICATES
# =====================================================

def remove_duplicates(items):

    unique = []

    for item in items:

        item = item.strip()

        if item and item not in unique:

            unique.append(item)

    return unique


# =====================================================
# EXTRACT RESUME SECTIONS
# =====================================================

def extract_sections(text):

    lines = clean_lines(text)

    education = []
    experience = []
    projects = []
    certificates = []
    skills = []

    # =====================================================
    # KEYWORDS
    # =====================================================

    education_keywords = [
        "education",
        "college",
        "university",
        "b.tech",
        "bachelor",
        "cgpa",
        "school"
    ]

    experience_keywords = [
        "experience",
        "internship",
        "work"
    ]

    project_keywords = [
        "project",
        "projects"
    ]

    certificate_keywords = [
        "certificate",
        "certification",
        "achievement"
    ]

    skill_keywords = [
        "skills",
        "technical skills",
        "programming",
        "languages",
        "tools",
        "technologies"
    ]

    # =====================================================
    # EXTRACT DATA
    # =====================================================

    for line in lines:

        lower = line.lower()

        # EDUCATION
        if any(word in lower for word in education_keywords):

            education.append(line)

        # EXPERIENCE
        elif any(word in lower for word in experience_keywords):

            experience.append(line)

        # PROJECTS
        elif any(word in lower for word in project_keywords):

            projects.append(line)

        # CERTIFICATES
        elif any(word in lower for word in certificate_keywords):

            certificates.append(line)

        # SKILLS
        elif any(word in lower for word in skill_keywords):

            skills.append(line)

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    education = remove_duplicates(education)

    experience = remove_duplicates(experience)

    projects = remove_duplicates(projects)

    certificates = remove_duplicates(certificates)

    skills = remove_duplicates(skills)

    return (
        education,
        experience,
        projects,
        certificates,
        skills
    )
