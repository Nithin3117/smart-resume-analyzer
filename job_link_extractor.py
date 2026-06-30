import requests
from bs4 import BeautifulSoup


def extract_job_text(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ")

        return text.lower()

    except:
        return ""
