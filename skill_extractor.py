def load_skills(file_path):
    with open(file_path, "r") as f:
        skills = [line.strip().lower() for line in f.readlines()]
    return skills

def extract_skills(tokens, skills_list):
    found_skills = []
    for token in tokens:
        if token.lower() in skills_list:
            found_skills.append(token.lower())
    return list(set(found_skills))
