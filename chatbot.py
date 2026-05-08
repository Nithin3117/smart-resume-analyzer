def chatbot_response(question):

    q = question.lower()

    # ATS
    if "ats" in q:

        return (
            "To improve ATS score, add job-description keywords, "
            "strong technical skills, and proper formatting."
        )

    # Skills
    elif "skill" in q:

        return (
            "Add skills related to your target job role such as "
            "Python, SQL, React, Machine Learning, or Cloud."
        )

    # Projects
    elif "project" in q:

        return (
            "Include 2–3 strong projects with technologies used, "
            "problem solved, and measurable outcomes."
        )

    # Experience
    elif "experience" in q:

        return (
            "Add internships, freelance work, or real-world practical experience."
        )

    # Resume
    elif "resume" in q:

        return (
            "Keep your resume concise, ATS-friendly, and focused on achievements."
        )

    # Jobs
    elif "job" in q:

        return (
            "Apply for jobs that match your strongest technical skills and projects."
        )

    # Default
    else:

        return (
            "Improve your resume using strong action verbs, "
            "ATS keywords, and clear formatting."
        )
