import smtplib


class Gmail():

    def __init__(self):
        self.mailserver = 'smtp.gmail.com:587'
        self._you = None
        self._to = []
        self._subject = None
        self._message = None
        self._messageTemplate = """\
From: {0}
To: {1}
Subject: {2}

{3}
"""

    def setFrom(self, you):
        self._you = you


    def addRecipient(self, recipent):
        self._to.append(recipent)


    def subject(self, subject):
        self._subject = subject


    def message(self, message):
        self._message = message


    def setAuth(self, username, password):
        self._username = username
        self._password = password


    def send(self):
        gm = smtplib.SMTP(self.mailserver)
        gm.starttls()

        gm.login(self._username, self._password)
        message = self._messageTemplate.format(self._you, ", ".join(self._to), self._subject, self._message)
        gm.sendmail(self._you, self._to, message)
        gm.quit()