import re
import nltk

from nltk.tokenize import word_tokenize

# =====================================================
# DOWNLOAD NLTK DATA
# =====================================================

try:
    nltk.data.find("tokenizers/punkt")

except LookupError:
    nltk.download("punkt")


# =====================================================
# PREPROCESS TEXT
# =====================================================

def preprocess(text):

    # Convert to lowercase
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Tokenize
    tokens = word_tokenize(text)

    return tokens


# =====================================================
# CLEAN LINES
# =====================================================

def clean_lines(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:

        # Remove extra spaces
        line = line.strip()

        # Ignore empty/small lines
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
    # SECTION KEYWORDS
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
        "work experience",
        "employment"
    ]

    project_keywords = [
        "project",
        "projects"
    ]

    certificate_keywords = [
        "certificate",
        "certification",
        "achievement",
        "achievements"
    ]

    skill_keywords = [
        "skills",
        "technical skills",
        "programming",
        "languages",
        "tools",
        "technologies",
        "frameworks"
    ]

    # =====================================================
    # EXTRACT DATA
    # =====================================================

    for line in lines:

        lower = line.lower()

        # EDUCATION
        if any(keyword in lower for keyword in education_keywords):

            education.append(line)

        # EXPERIENCE
        elif any(keyword in lower for keyword in experience_keywords):

            experience.append(line)

        # PROJECTS
        elif any(keyword in lower for keyword in project_keywords):

            projects.append(line)

        # CERTIFICATES
        elif any(keyword in lower for keyword in certificate_keywords):

            certificates.append(line)

        # SKILLS
        elif any(keyword in lower for keyword in skill_keywords):

            skills.append(line)

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    education = remove_duplicates(education)

    experience = remove_duplicates(experience)

    projects = remove_duplicates(projects)

    certificates = remove_duplicates(certificates)

    skills = remove_duplicates(skills)

    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return (
        education,
        experience,
        projects,
        certificates,
        skills
    )
