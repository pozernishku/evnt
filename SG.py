#!/usr/bin/env python3

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, CustomArg

message = Mail(
    from_email='zackushka@gmail.com',
    to_emails='toknow.top@gmail.com',
    subject='17Sending with Twilio SendGrid is Fun',
    html_content='<strong>17and easy to do anywhere, even with Python</strong>')

message.custom_arg = CustomArg('country', 'us')

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))