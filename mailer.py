import sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings

def send_email(caller, call_time):
    msg = MIMEMultipart()
    msg['From'] = settings.email_sender
    msg['To'] = settings.email_receiver
    msg['Subject'] = "Verpasster Anruf: " + str(caller)

    email_text = "Anrufer: " + str(caller) + "  Zeit/Datum: " + str(call_time) 
    msg.attach(MIMEText(email_text, 'html'))

    server = smtplib.SMTP_SSL(settings.mailserver, settings.mailserver_port)
    server.login(settings.mailserver_username, settings.mailserver_password)
    text = msg.as_string()
    server.sendmail(settings.email_sender, settings.email_receiver, text)
    server.quit()    

