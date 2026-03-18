def extract_job_skills(job_text,skills_list):

    job_text = job_text.lower()

    job_skills = []

    for skill in skills_list:

        if skill in job_text:

            job_skills.append(skill)

    return job_skills


def calculate_match(resume_skills,job_skills):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set.intersection(job_set)

    missing = job_set - resume_set

    if len(job_skills) == 0:

        score = 0

    else:

        score = (len(matched) / len(job_skills)) * 100

    return score,matched,missing
