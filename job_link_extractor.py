import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def clean_text(text):

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line and len(line) > 2:
            lines.append(line)

    return "\n".join(lines)


def extract_job_text(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except Exception:

        return ""


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # Remove unnecessary tags

    for tag in soup([
        "script",
        "style",
        "header",
        "footer",
        "nav",
        "svg",
        "noscript"
    ]):
        tag.decompose()


    text = soup.get_text(separator="\n")

    text = clean_text(text)

    print("FIRST 1000 CHARACTERS:")
    print(text[:1000])

    return text
