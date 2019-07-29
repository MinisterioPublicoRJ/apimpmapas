import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from decouple import config
from jinja2 import Template


def login():
    server = smtplib.SMTP(config('EMAIL_SMTP_SERVER'))
    return server


def send_mail(server, msg, dest, subject):
    msg_mime = MIMEMultipart('alternative')
    msg_mime.set_charset('utf8')
    msg_mime['FROM'] = config('EMAIL_HOST_USER')
    msg_mime['Subject'] = subject
    attach = MIMEText(msg.encode('utf-8'), 'html', 'UTF-8')
    msg_mime.attach(attach)
    server.sendmail(
        config('EMAIL_HOST_USER'),
        dest,
        msg_mime.as_string()
    )


with open('api/templates/api/email_dt.html') as fobj:
    dado_template = Template(fobj.read())

with open('api/templates/api/email_ent.html') as fobj:
    ent_template = Template(fobj.read())

with open('api/templates/api/email_map.html') as fobj:
    map_template = Template(fobj.read())
