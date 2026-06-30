import requests
from bs4 import BeautifulSoup

def extract_job_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    print(response.url)
    print(response.text[:500])

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text(separator=" ").lower()
