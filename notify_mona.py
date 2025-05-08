import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

#Get your email credentials
load_dotenv()
EMAIL = os.getenv('EMAIL')
PW = os.getenv('PW')
GMAIL_PW = os.getenv('GMAIL_PW')
first_name = "Mona"

#Email template
def create_email(first_name, dates):
    return f"""
<html>
  <body>
    <p>Hey {first_name}!</p>

    <p>Your Wimbledon tickets may be available!</p>

    <p>We found some availability on Centre Court for <strong>{available_date_time}.</strong></p>

    <p>Go get them at the <a href="https://ticketsale.wimbledon.com/content">Wimbledon Ticket Resale Site</a> before they're gone!</p>

    <p>Live your best tennis life!</p>
  </body>
</html>
"""

#Send the email
subject = "Wimbledon Tix!"

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(EMAIL, GMAIL_PW)

    message = MIMEMultipart()
    message["From"] = EMAIL
    message["To"] = EMAIL
    message["Subject"] = "Wimbledon Tix!"

    first_name="Mona"
    body = create_email(first_name, available_date_time)

    message.attach(MIMEText(body, "html"))

    server.sendmail(EMAIL, EMAIL, message.as_string())
    print("Email sent!")