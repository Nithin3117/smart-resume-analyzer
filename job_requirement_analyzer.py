import re

def extract_experience(text):

    pattern = r"\d+\+?\s*years"

    matches = re.findall(pattern,text)

    return matches


def extract_education(text):

    keywords = [
        "bachelor",
        "master",
        "phd",
        "b.tech",
        "m.tech",
        "degree"
    ]

    found = []

    for word in keywords:
        if word in text:
            found.append(word)

    return found


def extract_responsibilities(text):

    responsibilities = []

    lines = text.split(".")

    for line in lines:

        if "responsible" in line or "develop" in line or "build" in line:

            responsibilities.append(line.strip())

    return responsibilities[:5]
