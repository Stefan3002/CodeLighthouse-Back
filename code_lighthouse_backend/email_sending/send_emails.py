import asyncio
import smtplib, ssl, os

import aiohttp
from celery import shared_task
from dotenv import load_dotenv

port = 465  # For SSL

# Specify the full path to your .env file
dotenv_path = '../../.env'

# Load environment variables from .env file
load_dotenv(dotenv_path)

password = os.environ['EMAIL_PASSWORD']

# Create a secure SSL context
context = ssl.create_default_context()

sender_email = 'secrieru2302@gmail.com'

@shared_task
def send_email_async(receiver_email, message):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)

def send_email(receiver_email, message):
    send_email_async.apply_async(args=[receiver_email, message.as_string()], kwargs=[])



# send_email(receiver_email, message)