import requests
from bs4 import BeautifulSoup

def extract_job_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return text.lower()
    except:
        return ""
