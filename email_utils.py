import requests
import os

API_KEY = os.getenv("BREVO_API_KEY")  # from Streamlit secrets

def send_otp(email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Resume Analyzer",
            "email": "your_verified_email@gmail.com"
        },
        "to": [{"email": email}],
        "subject": "Your OTP Code",
        "htmlContent": f"<h2>Your OTP is: {otp}</h2>"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return True
    else:
        print("ERROR:", response.text)
        return False
