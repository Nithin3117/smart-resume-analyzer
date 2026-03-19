import smtplib
import random
from email.mime.text import MIMEText

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"


def send_otp(receiver_email):

    otp = str(random.randint(100000, 999999))

    msg = MIMEText(f"""
Your OTP is: {otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.
""")

    msg["Subject"] = "Secure OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return otp

    except Exception as e:
        print("Email Error:", e)
        return None
