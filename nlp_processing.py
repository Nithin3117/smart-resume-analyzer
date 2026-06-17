import re

# PREPROCESS TEXT

def preprocess(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.split()

# EXTRACT RESUME SECTIONS

def extract_sections(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if len(line) > 2:
            cleaned.append(line)
    education = []
    experience = []
    projects = []
    certificates = []
    skills = []
    for line in cleaned:
        lower = line.lower()

        # EDUCATION

        if any(word in lower for word in [
            "education",
            "college",
            "university",
            "b.tech",
            "cgpa"
        ]):
            education.append(line)

        # EXPERIENCE

        elif any(word in lower for word in [
            "experience",
            "internship",
            "work"
        ]):
            experience.append(line)

        # PROJECTS

        elif any(word in lower for word in [
            "project",
            "projects"
        ]):
            projects.append(line)

        # CERTIFICATES

        elif any(word in lower for word in [
            "certificate",
            "certification",
            "achievement"
        ]):
            certificates.append(line)

        # SKILLS

        elif any(word in lower for word in [
            "skills",
            "technical",
            "programming",
            "tools",
            "technologies"
        ]):
            skills.append(line)
    return (
        list(set(education)),
        list(set(experience)),
        list(set(projects)),
        list(set(certificates)),
        list(set(skills))
    )
