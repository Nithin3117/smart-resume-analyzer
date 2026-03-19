import smtplib
import random
from email.mime.text import MIMEText

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"   # Gmail App Password


def send_otp(receiver_email):

    otp = str(random.randint(100000, 999999))

    msg = MIMEText(f"Your OTP is: {otp}")
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

        print("OTP sent:", otp)  # debug

        return otp

    except Exception as e:
        print("Error:", e)
        return otp   # 🔥 return OTP anyway for demo
