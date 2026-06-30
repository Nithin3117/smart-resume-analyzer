import requests
from bs4 import BeautifulSoup

def extract_job_text(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    print("=" * 80)
    print("STATUS:", response.status_code)
    print("FINAL URL:", response.url)
    print("=" * 80)
    print(response.text[:1000])
    print("=" * 80)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text(separator=" ")
    
