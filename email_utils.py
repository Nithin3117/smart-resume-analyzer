import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import random

# 🔑 Your Brevo API Key
BREVO_API_KEY = "xkeysib-REPLACE_WITH_YOUR_KEY"

# 📧 Verified sender email
SENDER_EMAIL = "nithinbollineni04@gmail.com"


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
        print("STATUS:", response)
        print("OTP:", otp)
        return otp

    except ApiException as e:
        print("ERROR:", e)
        return None
