import smtplib
import random
from email.mime.text import MIMEText

# 🔥 REPLACE THESE
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # MUST be Gmail App Password


def send_otp(receiver_email):

    otp = str(random.randint(100000, 999999))

    msg = MIMEText(f"""
Your OTP is: {otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.
""")

    msg["Subject"] = "OTP Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        print("OTP SENT:", otp)  # DEBUG
        return otp

    except Exception as e:
        print("EMAIL ERROR:", e)
        return None
