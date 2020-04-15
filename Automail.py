# Python code to illustrate Sending mail from
# your Gmail account
import smtplib, ssl

class Mailer:

    def __init__(self):
        self.EMAIL = "_"
        self.PASS = "_"
        self.PORT = 465
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.PORT)

    def send(self, user_name, parents_mail):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.PORT)
        self.server.login(self.EMAIL, self.PASS)
        # message to be sent
        SUBJECT = 'Absense Report'
        TEXT = f'Your child {user_name} has been absent today!'
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        # sending the mail
        self.server.sendmail(self.EMAIL, parents_mail, message)
        self.server.quit()
