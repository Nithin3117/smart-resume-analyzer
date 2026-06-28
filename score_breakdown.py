def calculate_breakdown(
    score,
    matched,
    missing,
    education,
    experience,
    projects
)

    # ATS SCORE
    ats_score = int(score)

    # SKILLS SCORE
    total_skills = len(matched) + len(missing)
    if total_skills == 0:
        skills_score = 0
    else:
        skills_score = int(
            (len(matched) / total_skills) * 100
        )

    # EDUCATION SCORE
    education_score = 0
    if education:
        for item in education:
            text = item.lower()
            if "b.tech" in text or "btech" in text:
                education_score += 50
            elif "intermediate" in text or "+2" in text:
                education_score += 25
            elif "ssc" in text or "10th" in text:
                education_score += 25
            elif "cgpa" in text or "%" in text:
                education_score += 10
        education_score = min(education_score, 100)

    # EXPERIENCE SCORE
    experience_score = 0
    if experience:
        experience_score = min(
            len(experience) * 30,
            100
        )

    # PROJECT SCORE
    project_score = 0
    if projects:
        project_score = min(
            len(projects) * 30,
            100
        )

    return {
        "ATS Compatibility": ats_score,
        "Skills Match": skills_score,
        "Education Strength": education_score,
        "Experience Strength": experience_score,
        "Project Strength": project_score

    }
