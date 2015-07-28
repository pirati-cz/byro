#!/usr/bin/env python3

import re
import smtplib
from getpass import getpass
from markdown import Markdown
from email.message import EmailMessage


class Mail:

    def __init__(self, frm, login, recipients="recipients.txt", body="advance-body.md"):
        self.frm = frm
        self.login = login
        self.recipients = self._read_recipients_from_file(recipients)
        self.content = self._read_markdown_body(body)
        pass

    def send(self):
        msg = self._prepare_message()
        passwd = getpass()

        try:
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(self.login, passwd)
            server.send_message(msg)
            server.close()
            print('Successfully sent the mail')
        except Exception as e:
            print("Failed to send mail:")
            print(e)

    def _prepare_message(self):
        msg = EmailMessage()
        msg['From'] = self.frm
        msg['To'] = self.recipients
        content = self.content
        msg['Subject'] = content['meta']['subject'][0]
        msg.set_content(content['raw'])
        msg.add_alternative(content['html'], subtype='html')
        return msg

    @staticmethod
    def _read_recipients_from_file(filename):
        mail = "[^@]+@[^@]+\.[^@]+"

        if re.match(mail, filename):
            return [filename]
        else:
            with open(filename) as f:
                return list(line.rstrip('\n') for line in f)

    @staticmethod
    def _read_markdown_body(filename):
        with open(filename) as f:
            text1 = f.read()

        md = Markdown(extensions = ['markdown.extensions.meta'])
        text2 = md.convert(text1)

        return {'raw': text1, 'html': text2, 'meta': md.Meta}

if __name__ == "__main__":
    pass