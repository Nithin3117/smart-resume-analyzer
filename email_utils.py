import requests
import random
import time
import streamlit as st

# ==============================
# BREVO CONFIG
# ==============================

BREVO_API_KEY = st.secrets["BREVO_API_KEY"]

# Verified sender email in Brevo
SENDER_EMAIL = "yourverifiedemail@gmail.com"


# ==============================
# GENERATE OTP
# ==============================

def generate_otp():
    return str(random.randint(100000, 999999))


# ==============================
# SEND OTP EMAIL
# ==============================

def send_otp_email(receiver_email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Smart Resume Analyzer",
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": "Your OTP Verification Code",

        "htmlContent": f"""
        <div style="
            font-family: Arial;
            padding: 20px;
            background-color: #f4f7ff;
            border-radius: 10px;
        ">

            <h2 style="color:#4F46E5;">
                Resume Analyzer OTP Verification
            </h2>

            <p>Your OTP code is:</p>

            <h1 style="
                letter-spacing: 5px;
                color:#111827;
            ">
                {otp}
            </h1>

            <p>This OTP is valid for 5 minutes.</p>

            <br>

            <p style="font-size:13px;color:gray;">
                If you did not request this OTP,
                please ignore this email.
            </p>

        </div>
        """
    }

    # ==============================
    # RETRY LOGIC
    # ==============================

    for attempt in range(3):

        try:

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=15
            )

            print("BREVO RESPONSE:", response.text)

            if response.status_code == 201:
                return True

            else:
                print("Brevo Error:", response.text)

        except Exception as e:

            print("OTP ERROR:", str(e))

        time.sleep(2)

    return False
