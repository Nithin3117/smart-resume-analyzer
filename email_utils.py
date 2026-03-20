from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random

# 🔑 Replace with your actual SendGrid API Key
SENDGRID_API_KEY = "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"

# 📧 Must be VERIFIED in SendGrid
SENDER_EMAIL = "nithinbollineni04@gmail.com"


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_otp(receiver_email):
    """Send OTP to user email"""

    otp = generate_otp()

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=receiver_email,
        subject="🔐 Your OTP Code - Smart Resume Analyzer",
        html_content=f"""
        <div style="font-family: Arial; padding: 20px;">
            <h2 style="color: #4CAF50;">Smart Resume Analyzer</h2>
            <p>Your OTP for login/signup is:</p>
            <h1 style="color: #333;">{otp}</h1>
            <p>This OTP is valid for a short time.</p>
            <br>
            <p>If you didn’t request this, ignore this email.</p>
        </div>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # 🔍 Debug logs (VERY IMPORTANT)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE BODY:", response.body)
        print("OTP SENT:", otp)

        # ✅ Success check
        if response.status_code == 202:
            return otp
        else:
            return None

    except Exception as e:
        print("❌ ERROR SENDING EMAIL:", str(e))
        return None
