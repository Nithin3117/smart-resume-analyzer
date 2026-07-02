import re

def calculate_breakdown(
    score,
    matched,
    missing,
    education,
    experience,
    projects
):

    # ATS SCORE 

    ats_score = max(0, min(int(score), 100))

    # SKILLS SCORE 
  
    total_skills = len(matched) + len(missing)

    if total_skills == 0:
        skills_score = 0
    else:
        skills_score = round(
            (len(matched) / total_skills) * 100
        )

    # EDUCATION SCORE 

    education_score = 0
    edu_text = " ".join(education).lower()

    # Degree

    if any(
        word in edu_text
        for word in [
            "b.tech",
            "btech",
            "b.e",
            "be ",
            "bachelor"
        ]
    ):
        education_score += 35

    # Intermediate

    if any(
        word in edu_text
        for word in [
            "intermediate",
            "12th",
            "+2"
        ]
    ):
        education_score += 20

    # School

    if any(
        word in edu_text
        for word in [
            "ssc",
            "10th",
            "secondary"
        ]
    ):
        education_score += 15

    # Marks / CGPA

    if re.search(r"cgpa|gpa|percentage|%", edu_text):
        education_score += 15

    # College

    if any(
        word in edu_text
        for word in [
            "university",
            "college",
            "institute"
        ]
    ):
        education_score += 15
    education_score = min(education_score, 100)

    # EXPERIENCE SCORE 

    experience_score = 0
    exp_text = " ".join(experience).lower()
    if exp_text:
        if any(
            word in exp_text
            for word in [
                "intern",
                "internship"
            ]
        ):
            experience_score += 40
        if any(
            word in exp_text
            for word in [
                "software",
                "developer",
                "engineer",
                "analyst"
            ]
        ):
            experience_score += 30

        years = re.findall(
            r"\d+\+?\s*(?:year|years|month|months)",
            exp_text
        )

        if years:
            experience_score += 30

        experience_score = min(
            experience_score,
            100
        )

    # PROJECT SCORE 

    project_score = 0
    project_text = " ".join(projects).lower()
    if project_text:
        project_score += min(
            len(projects) * 20,
            40
        )
        technologies = [
            "python",
            "java",
            "c++",
            "streamlit",
            "tensorflow",
            "flask",
            "django",
            "sql",
            "mysql",
            "mongodb",
            "html",
            "css",
            "javascript",
            "react",
            "node"
        ]

        tech_count = 0
        for tech in technologies:
            if tech in project_text:
                tech_count += 1
        project_score += min(
            tech_count * 5,
            30
        )
        if (
            "github" in project_text
            or "live" in project_text
            or "deployed" in project_text
        ):
            project_score += 15
        if len(project_text) > 250:
            project_score += 15
        project_score = min(
            project_score,
            100
        )
    return {
        "ATS Compatibility": ats_score,
        "Skills Match": skills_score,
        "Education Strength": education_score,
        "Experience Strength": experience_score,
        "Project Strength": project_score
    }
