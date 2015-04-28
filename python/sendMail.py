#!/usr/bin/python

import smtplib
import sys

GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

GMAIL_EMAIL = "onlyjigar2772@gmail.com"
GMAIL_PASSWORD = ""

def initialize_smtp_server():
    smtpserver = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(GMAIL_EMAIL, GMAIL_PASSWORD)
    return smtpserver

def send_thank_you_mail():
    to_email = 'jigar.shah\@wipro.com'
    email = 'jigar.shah\@wipro.com'
    from_email = GMAIL_EMAIL
    subj = "This is a test mail"
    header = "To:%s\nFrom:%s\nSubject:%s \n" % (to_email,
            from_email, subj)
    # Hard-coded templates are not best practice.
    msg_body = """
    Hi %s,

    Thank you very much for your repeated comments on our service.
    The interaction is much appreciated.

    Thank You.""" % email
    content = header + "\n" + msg_body
    smtpserver = initialize_smtp_server()
    smtpserver.sendmail(from_email, to_email, content)
    smtpserver.close()
    
if __name__ == "__main__":
    send_thank_you_mail()
