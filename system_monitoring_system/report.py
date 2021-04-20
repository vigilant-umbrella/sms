from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from exceptions import AuthenticationError
import helper
import os
import smtplib


def down_report(resource='Main Menu'):
    pdf = helper.create_report(resource)

    download_folder = ''
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        download_folder = location
    else:
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    filename = '/report_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.pdf'
    pdf.output(download_folder+filename, 'F')


def send_email(email, password, resource='Main Menu'):
    pdf = helper.create_report(resource)

    filename = 'report_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.pdf'

    receivers = ['bcs_2019008@iiitm.ac.in',
                 'bcs_2019075@iiitm.ac.in', 'bcs_2019025@iiitm.ac.in']

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'System Monitoring System'
    message['To'] = ', '.join(receivers)
    message['Subject'] = 'Report - System Monitoring System'

    body = """
    Hi,

    Please find attached the report you requested.

    Regards,
    System Monitoring System Team
    """

    message.attach(MIMEText(body, 'plain'))

    payload = MIMEBase('application', 'octate-stream', Name=filename)
    payload.set_payload(pdf.output(filename, 'S'))

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition',
                       'attachment', filename=filename)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # enable security
    session.starttls()

    # login with mail_id and password
    try:
        session.login(email, password)
    except smtplib.SMTPAuthenticationError:
        msg = """
        Either of the following error occured:
          1. Username or password do not match to an existing Google account.
          2. Less secure app access is turned off.
        """
        raise AuthenticationError(msg)

    text = message.as_string()
    try:
        session.sendmail(email, receivers, text)
    except smtplib.SMTPSenderRefused:
        msg = """
        Either of the following error occured:
          1. Username or password do not match to an existing Google account.
          2. Less secure app access is turned off.
        """
        raise AuthenticationError(msg)

    session.quit()
    print('Mail Sent')


if __name__ == '__main__':
    exit()
