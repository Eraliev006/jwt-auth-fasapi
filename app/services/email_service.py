import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
from app.core import settings

email_sender_logger = getLogger('project.email_sender_service')

def send_email(
               receiver_email: str,
               subject: str,
               body: str,
               sender_email: str = settings.smtp.sender_email,
               smtp_server: str = settings.smtp.smtp_server,
               smtp_port: int = settings.smtp.smtp_port,
               login: str = settings.smtp.smtp_login,
               password: str = settings.smtp.smtp_password):

    server = None

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        email_sender_logger.info('Trying to send email')
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        email_sender_logger.info('Email successfully sent')
    except Exception:
        email_sender_logger.exception('Problem with sending email: ')
        raise
    finally:
        if server:
            server.quit()
