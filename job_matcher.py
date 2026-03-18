def load_job_description(file_path):
    with open(file_path, "r") as file:
        text = file.read().lower()
    return text


def extract_job_skills(job_text, skills_list):

    job_skills = []

    for skill in skills_list:
        if skill in job_text:
            job_skills.append(skill)

    return job_skills


def calculate_match(resume_skills, job_skills):

    matched = set(resume_skills) & set(job_skills)

    score = (len(matched) / len(job_skills)) * 100

    missing_skills = set(job_skills) - set(resume_skills)

    return score, matched, missing_skills