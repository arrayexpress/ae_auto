import settings
import smtplib
from email.mime.text import MIMEText

__author__ = 'Ahmed G. Ali'


def send_email(from_email, to_emails, subject, body):
    """
    Sends an email

    :param from_email: sender email which must be an `EBI` email
    :type from_email: str
    :param to_emails: list of receiver emails
    :type to_emails: :obj:`list` of :obj:`str`
    :param subject: Subject of the email.
    :type subject: str
    :param body: String formatted body text.
    :type body: str

    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ','.join(to_emails)

    s = smtplib.SMTP(settings.SMTP)
    s.sendmail(from_email, to_emails, msg.as_string())
    s.quit()
    # print 'email sent!'


if __name__ == '__main__':
    send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>', to_emails=['ahmed@ebi.ac.uk', 'eng.gemmy@gmail.com'],
               subject='Test Subject',
               body="""Dear Curator,
Thank you!.
Ahmed.""")
