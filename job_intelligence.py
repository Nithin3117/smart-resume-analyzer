import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_job_keywords(job_text, skills_list):
    text = clean_text(job_text)

    found_skills = []

    for skill in skills_list:
        skill_clean = skill.lower().strip()

        if not skill_clean:
            continue

        pattern = r"(?<!\w)" + re.escape(skill_clean) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return list(dict.fromkeys(found_skills))


def extract_job_sections(job_text):
    text = job_text.replace("\r", "\n")

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    sections = {
        "responsibilities": [],
        "requirements": [],
        "preferred": [],
        "qualifications": []
    }

    current_section = None

    section_keywords = {
        "responsibilities": [
            "responsibilities",
            "responsibility",
            "role and responsibilities",
            "what you will do",
            "what you'll do",
            "duties"
        ],
        "requirements": [
            "requirements",
            "required skills",
            "required qualifications",
            "must have",
            "required"
        ],
        "preferred": [
            "preferred skills",
            "preferred qualifications",
            "nice to have",
            "good to have",
            "preferred"
        ],
        "qualifications": [
            "qualifications",
            "education",
            "educational qualifications"
        ]
    }

    for line in lines:

        clean_line = line.lower().strip()

        clean_line = re.sub(
            r"[:\-]+$",
            "",
            clean_line
        ).strip()

        found_section = None

        for section, keywords in section_keywords.items():

            if clean_line in keywords:
                found_section = section
                break

        if found_section:
            current_section = found_section
            continue

        if current_section:

            cleaned_line = re.sub(
                r"^[•●◦▪➤▶♦★✓✔\-\*]+",
                "",
                line
            ).strip()

            if cleaned_line:
                sections[current_section].append(
                    cleaned_line
                )

    return sections


def calculate_keyword_match(resume_text, job_keywords):
    resume_text = clean_text(resume_text)

    if not job_keywords:
        return 0, [], []

    matched = []
    missing = []

    for keyword in job_keywords:

        keyword_clean = keyword.lower().strip()

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword_clean)
            + r"(?!\w)"
        )

        if re.search(pattern, resume_text):
            matched.append(keyword)
        else:
            missing.append(keyword)

    score = round(
        (len(matched) / len(job_keywords)) * 100
    )

    return score, matched, missing


def extract_job_level(job_text):
    text = clean_text(job_text)

    patterns = [
        (
            "internship",
            [
                "intern",
                "internship",
                "trainee"
            ]
        ),
        (
            "entry level",
            [
                "entry level",
                "fresher",
                "0-1 years",
                "0–1 years",
                "0 to 1 years",
                "1 year experience"
            ]
        ),
        (
            "junior",
            [
                "junior developer",
                "junior software",
                "junior engineer"
            ]
        ),
        (
            "mid level",
            [
                "2-5 years",
                "3-5 years",
                "mid level",
                "mid-level"
            ]
        ),
        (
            "senior",
            [
                "senior developer",
                "senior engineer",
                "5+ years",
                "5 years experience"
            ]
        )
    ]

    for level, keywords in patterns:

        for keyword in keywords:

            if keyword in text:
                return level

    return "Not specified"


def extract_experience_requirement(job_text):
    text = clean_text(job_text)

    patterns = [
        r"(\d+)\s*\+\s*years?",
        r"(\d+)\s*-\s*(\d+)\s*years?",
        r"(\d+)\s*to\s*(\d+)\s*years?",
        r"(\d+)\s*years?\s+of\s+experience"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            numbers = [
                int(value)
                for value in match.groups()
                if value
            ]

            if len(numbers) == 1:
                return f"{numbers[0]}+ years"

            if len(numbers) == 2:
                return (
                    f"{numbers[0]}-{numbers[1]} years"
                )

    return "Not specified"


def analyze_job_description(
    job_text,
    skills_list,
    resume_text=""
):
    job_keywords = extract_job_keywords(
        job_text,
        skills_list
    )

    sections = extract_job_sections(
        job_text
    )

    job_level = extract_job_level(
        job_text
    )

    experience_requirement = (
        extract_experience_requirement(
            job_text
        )
    )

    if resume_text:

        keyword_score, matched, missing = (
            calculate_keyword_match(
                resume_text,
                job_keywords
            )
        )

    else:

        keyword_score = 0
        matched = []
        missing = []

    return {
        "job_keywords": job_keywords,
        "sections": sections,
        "job_level": job_level,
        "experience_requirement": experience_requirement,
        "keyword_score": keyword_score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }