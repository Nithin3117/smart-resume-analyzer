import PyPDF2
from nlp_processing import preprocess
from skill_extractor import load_skills, extract_skills
from job_matcher import load_job_description, extract_job_skills, calculate_match


def extract_text(pdf_file):

    text = ""

    with open(pdf_file, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text += page.extract_text()

    return text


# extract resume text
resume_text = extract_text("resume.pdf")


# NLP processing
tokens = preprocess(resume_text)


# load skills database
skills_list = load_skills("skills.txt")


# detect skills from resume
resume_skills = extract_skills(tokens, skills_list)


# load job description
job_text = load_job_description("job_description.txt")


# detect job required skills
job_skills = extract_job_skills(job_text, skills_list)


# calculate match
score, matched, missing = calculate_match(resume_skills, job_skills)


print("\nResume Skills Detected:")
print(resume_skills)

print("\nJob Required Skills:")
print(job_skills)

print("\nMatched Skills:")
print(list(matched))

print("\nMissing Skills:")
print(list(missing))

print("\nResume Match Score:")
print(score, "%")