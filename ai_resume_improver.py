def improve_resume(
        missing_skills,
        education,
        experience,
        projects,
        resume_text
):
    improvements = []

    # Missing Skills
    if missing_skills:
        improvements.append(
            f"Add important skills like {', '.join(missing_skills[:5])} to improve ATS compatibility."
        )

    # Education
    if not education:
        improvements.append(
            "Add clear education details with degree, college, and graduation year."
        )

    # Experience
    if not experience:
        improvements.append(
            "Include internships, freelance work, or practical experience."
        )

    # Projects
    if not projects:
        improvements.append(
            "Add 2–3 strong projects with technologies used and achievements."
        )

    # Resume length
    words = len(resume_text.split())
    if words < 150:
        improvements.append(
            "Your resume is too short. Add more technical details and achievements."
        )

    elif words > 700:
        improvements.append(
            "Your resume is too lengthy. Keep it concise and ATS-friendly."
        )

    # Action verbs
    improvements.append(
        "Use strong action verbs like Developed, Implemented, Designed, Optimized."
    )

    # Formatting
    improvements.append(
        "Maintain proper headings and consistent formatting."
    )

    # Keywords
    improvements.append(
        "Use job-description keywords naturally throughout the resume."
    )
    return improvements
