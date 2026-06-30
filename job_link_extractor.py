import requests
from playwright.sync_api import sync_playwright


def extract_job_text(url):

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            text = page.locator("body").inner_text()

            browser.close()

            return text.lower()

    except Exception as e:

        print(e)

        return ""
