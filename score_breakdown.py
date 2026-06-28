def calculate_breakdown(
    score,
    matched,
    missing,
    education,
    experience,
    projects
):
    return {
        "ATS Compatibility": int(score),
        "Skills Match": 0,
        "Education Strength": 0,
        "Experience Strength": 0,
        "Project Strength": 0,
    }
