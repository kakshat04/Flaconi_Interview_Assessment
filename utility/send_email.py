import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


class EmailTest:
    def __init__(self, email_recipient, email_subject, email_message, attachment_location=''):
        self.email_recipient = email_recipient
        self.email_subject = email_subject
        self.email_message = email_message
        self.attachment_location = attachment_location

    def send_email(self):
        email_sender = 'kumar.akshat04@gmail.com'

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = self.email_recipient
        msg['Subject'] = self.email_subject

        msg.attach(MIMEText(self.email_message, 'plain'))

        if self.attachment_location != '':
            filename = os.path.basename(self.attachment_location)
            attachment = open(self.attachment_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email_sender, "moti@chotu")
            text = msg.as_string()
            server.sendmail(email_sender, self.email_recipient, text)
            print('email sent')
            server.quit()
        except:
            print("SMPT server connection error")
        return True


if __name__ == '__main__':
    email = EmailTest('kumar.akshat04@gmail.com', 'Test Email', 'Execution Report', r'F:\LeanIX_Assessment\Report.html')
    email.send_email()
