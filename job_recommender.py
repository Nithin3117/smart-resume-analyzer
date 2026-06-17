def recommend_jobs(skills):

    jobs = []
    skill_text = " ".join(skills).lower()

    # PYTHON

    if "python" in skill_text:
        jobs.append({
            "title": "Python Developer",
            "link": "https://in.indeed.com/jobs?q=python+developer"
        })

    # FRONTEND

    if "html" in skill_text or "css" in skill_text:
        jobs.append({
            "title": "Frontend Developer",
            "link": "https://in.indeed.com/jobs?q=frontend+developer"
        })

    # MACHINE LEARNING
  
    if "machine" in skill_text or "nlp" in skill_text:
        jobs.append({
            "title": "AI / Machine Learning Engineer",
            "link": "https://in.indeed.com/jobs?q=machine+learning+engineer"
        })

    # JAVA

    if "java" in skill_text:
        jobs.append({
            "title": "Java Developer",
            "link": "https://in.indeed.com/jobs?q=java+developer"
        })

    # DATA SCIENCE

    if "data" in skill_text:
        jobs.append({
            "title": "Data Scientist",
            "link": "https://in.indeed.com/jobs?q=data+scientist"
        })

    # DEFAULT

    if not jobs:
        jobs.append({
            "title": "Software Developer",
            "link": "https://in.indeed.com/jobs?q=software+developer"
        })
    return jobs
