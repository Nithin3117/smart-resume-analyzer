from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random

SENDGRID_API_KEY = "PASTE_YOUR_API_KEY"
SENDER_EMAIL = "nithinbollineni04@gmail.com"


def send_otp(receiver_email):

    otp = str(random.randint(100000, 999999))

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=receiver_email,
        subject="Your OTP Code",
        html_content=f"<h2>Your OTP is: {otp}</h2>"
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print("STATUS CODE:", response.status_code)
        print("RESPONSE BODY:", response.body)
        print("OTP SENT:", otp)

        return otp

    except Exception as e:
        print("FULL ERROR:", str(e))   # 🔥 VERY IMPORTANT
        return None
