def calculate_breakdown(
    score,
    matched,
    missing,
    education,
    experience,
    projects
):

    # -------------------------
    # ATS SCORE
    # -------------------------

    ats_score = int(score)

    # -------------------------
    # SKILLS SCORE
    # -------------------------

    total_skills = len(matched) + len(missing)

    if total_skills == 0:
        skills_score = 0
    else:
        skills_score = int(
            (len(matched) / total_skills) * 100
        )

    # -------------------------
    # EDUCATION SCORE
    # -------------------------

    education_score = 0

    if education:

        has_degree = False
        has_inter = False
        has_school = False
        has_marks = False

        for item in education:

            text = item.lower()

            if (
                "b.tech" in text
                or "btech" in text
                or "b.e" in text
                or "be " in text
                or "bachelor" in text
            ):
                has_degree = True

            if (
                "intermediate" in text
                or "+2" in text
                or "12th" in text
            ):
                has_inter = True

            if (
                "ssc" in text
                or "10th" in text
                or "secondary"
            ):
                has_school = True

            if (
                "cgpa" in text
                or "%"
                in text
            ):
                has_marks = True

        if has_degree:
            education_score += 40

        if has_inter:
            education_score += 20

        if has_school:
            education_score += 20

        if has_marks:
            education_score += 20

    # -------------------------
    # EXPERIENCE SCORE
    # -------------------------

    experience_score = 0

    if experience:

        count = len(experience)

        if count == 1:
            experience_score = 30

        elif count == 2:
            experience_score = 60

        elif count >= 3:
            experience_score = 100

    # -------------------------
    # PROJECT SCORE
    # -------------------------

    project_score = 0

    if projects:

        total = len(projects)

        if total == 1:
            project_score = 35

        elif total == 2:
            project_score = 65

        elif total >= 3:
            project_score = 100

    # -------------------------
    # RETURN
    # -------------------------

    return {

        "ATS Compatibility": ats_score,

        "Skills Match": skills_score,

        "Education Strength": education_score,

        "Experience Strength": experience_score,

        "Project Strength": project_score

    }
