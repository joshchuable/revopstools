#!/usr/bin/env python
# encoding: utf-8
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import datetime
import sys

# Get today's date formatted YYYY-MM-DD.
today = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

COMMASPACE = ', '

def send_gmail(attachments):
    sender = 'rye.jones@answers.com'
    gmail_password = 'PASSWORD'
    recipients = ['rvoa@answers.com','rye.jones@answers.com']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Rubicon Daily Update - %s' % today
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'Begin email.\n'

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments.")
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email.")
        raise