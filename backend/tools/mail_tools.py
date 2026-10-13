import os
import smtplib
from email.message import EmailMessage
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def send_email(to_mail : str, subject : str, body:str) -> str:
    """Send an email using Gmail SMTP

    Args:
        to_email : The recipient email address.
        subject : The subject line of the mail.
        body : The plain text body message of the email.
    """

    smtp_server = os.environ.get("SMTP_SERVER")
    smpt_port = os.environ.get("SMTP_PORT")
    sender_gmail = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_gmail or not sender_password:
        return "Error : SENDER EMAIL or SENDER PASSOWRD environment variables are not configured."

    try:
        msg = EmailMessage()
        msg["From"] = sender_gmail
        msg["To"] = to_mail
        msg["subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_server,smpt_port) as server:
            server.starttls()
            server.login(sender_gmail,sender_password)
            server.send_message(msg)

        return f"Email send successfully to {to_mail}."
    except Exception as e:
        return f"Failed to send an email : {str(e)}"    