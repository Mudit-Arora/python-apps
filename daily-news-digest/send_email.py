import ssl, smtplib
import os
from dotenv import load_dotenv
load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = email_address
    password = email_password

    receiver = email_address
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)