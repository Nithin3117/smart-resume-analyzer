def calculate_breakdown(
        score,
        matched,
        missing,
        education,
        experience,
        projects
):

    # ATS score
    ats_score = int(score)

    # Skills score
    if len(matched) + len(missing) > 0:
        skill_score = int(
            (len(matched) /
            (len(matched) + len(missing))) * 100
        )
    else:
        skill_score = 0

    # Education score
    education_score = 90 if education else 40

    # Experience score
    experience_score = 85 if experience else 35

    # Project score
    project_score = 90 if projects else 40

    return {
        "ATS Compatibility": ats_score,
        "Skills Match": skill_score,
        "Education Strength": education_score,
        "Experience Strength": experience_score,
        "Project Strength": project_score
    }
