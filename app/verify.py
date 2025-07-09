import smtplib
import random
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

otp_store = {}

def generate_otp(email: str) -> int:
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    return otp

def send_otp_email(email: str, otp: int):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        subject = "Memory Mosaic OTP Verification"
        body = f"Your OTP for Memory Mosaic registration is: {otp}"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL, email, message)

def verify_otp(email: str, otp: int) -> bool:
    return otp_store.get(email) == otp
