import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import streamlit as st
import random

# 🔐 Read from Streamlit secrets
BREVO_API_KEY = st.secrets["BREVO_API_KEY"]
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(receiver_email):
    otp = generate_otp()

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": receiver_email}],
        sender={"email": SENDER_EMAIL},
        subject="🔐 OTP Verification",
        html_content=f"<h2>Your OTP is: {otp}</h2>"
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("SUCCESS:", response)
        return otp

    except ApiException as e:
        print("ERROR:", e)
        return None
