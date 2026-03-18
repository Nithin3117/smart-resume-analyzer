def load_skills(file_path):
    with open(file_path, "r") as file:
        skills = file.read().splitlines()
    return skills


def extract_skills(tokens, skills_list):

    found_skills = []

    for skill in skills_list:
        if skill in tokens:
            found_skills.append(skill)

    return found_skills