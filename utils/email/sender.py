import settings
import smtplib
from email.mime.text import MIMEText

__author__ = 'Ahmed G. Ali'


def send_email(from_email, to_emails, subject, body):
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
