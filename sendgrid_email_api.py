# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()


def sendgrid_mail(to_email, html_content):

    logging.info(f"Constructing the mail")
    message = Mail(
        from_email=os.environ.get("FROM_EMAIL"),
        to_emails=to_email,
        subject="Today's auto-generated summary/tasks",
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        logging.info(f"Sending a mail to {to_email}")
        response = sg.send(message)
        print(response.body)
        print(response.headers)
        return response.status_code
    except Exception as e:
        return e.message
