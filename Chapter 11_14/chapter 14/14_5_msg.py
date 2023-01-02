import smtplib
from email.mime.multipart import MIMEMultipart  # install package
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
from configparser import ConfigParser
import base64


def get_config(env):
    config = ConfigParser.ConfigParser()
    if env == "DEV":
        config.read(['config/development.cfg'])
    elif env == "PROD":
        config.read(['config/production.cfg'])
    return config


def mail(to, subject, text, attach=None, config=None):
    if not config:
        config = get_config("DEV")
    msg = MIMEMultipart()
    msg['From'] = config.get('email', 'user')
    msg['To'] = ", ".join(to)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        # Encoders.encode_base64(part)
        # base64.b64encode(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(config.get('email', 'user'),
                     config.get('email', 'password'))
    mailServer.sendmail(config.get('email', 'user'), to, msg.as_string())
    mailServer.close()


def example():
    mail(['listof@mydomain.com', 'emails@mydomain.com'],
         "Automate your life: sending emails",
         "Why'd the elephant sit on the marshmallow?",
         attach="my_file.txt")
