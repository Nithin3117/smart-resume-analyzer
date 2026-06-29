import re


def extract_job_skills(job_text, skills_list):

    if not job_text:
        return []

    job_text = job_text.lower()

    found_skills = []

    for skill in skills_list:

        skill = skill.lower()

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, job_text):

            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def extract_required_experience(job_text):

    if not job_text:
        return None

    job_text = job_text.lower()

    patterns = [

        r'(\d+)\+?\s*years',

        r'(\d+)\+?\s*year',

        r'(\d+)\+?\s*yrs',

        r'(\d+)\+?\s*yr'

    ]

    for pattern in patterns:

        match = re.search(pattern, job_text)

        if match:

            return int(match.group(1))

    return 0


def extract_required_education(job_text):

    if not job_text:
        return []

    job_text = job_text.lower()

    education = []

    keywords = [

        "b.tech",

        "btech",

        "b.e",

        "be",

        "bachelor",

        "m.tech",

        "mtech",

        "master",

        "degree"

    ]

    for word in keywords:

        if word in job_text:

            education.append(word)

    return list(set(education))


def calculate_match(resume_skills, job_skills):

    resume = set([x.lower() for x in resume_skills])

    job = set([x.lower() for x in job_skills])

    matched = sorted(list(resume & job))

    missing = sorted(list(job - resume))

    if len(job) == 0:

        score = 0

    else:

        score = round(

            (len(matched) / len(job)) * 100

        )

    return score, matched, missing
