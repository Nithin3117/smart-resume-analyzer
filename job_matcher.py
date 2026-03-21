def extract_job_skills(job_text, skills_list):
    job_text = job_text.lower()
    job_skills = []

    for skill in skills_list:
        if skill.lower() in job_text:
            job_skills.append(skill)

    return job_skills


def calculate_match(resume_skills, job_skills):

    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    if len(job_set) == 0:
        return 0, [], []

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    score = (len(matched) / len(job_set)) * 100

    return score, matched, missing
