#!/usr/bin/env python3

import re
import time
import smtplib
from getpass import getpass
from markdown import Markdown
from email.message import EmailMessage


def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]


class Mail:
	def __init__(self, login, frm, **kwargs):
		self._limit = kwargs.get('limit', 35)
		self._delay = kwargs.get('delay', 35)
		self.frm = frm
		self.login = login
		self.server = kwargs.get('server', None)
		rec = kwargs.get('recipients', None)
		self.recipients = self._read_recipients_from_file(rec)
		bod = kwargs.get('body', None)
		self.content = self._read_markdown_body(bod[0])

	def send(self):
		msgs = self._prepare_message()
		passwd = getpass()

		try:
			# server = smtplib.SMTP(SERVER)
			server = smtplib.SMTP(self.server, 587)
			# or port 465 doesn't seem to work!
			server.ehlo()
			server.starttls()
			server.login(self.login, passwd)
			first = True
			for msg in msgs:
				if first:
					first = False
				else:
					print("Send next group of mails")
					time.sleep(self._delay)
				server.send_message(msg)

			server.close()
			print('Successfully sent the mail')
		except Exception as e:
			print("Failed to send mail:")
			print(e)
		finally:
			del (passwd)

	def _prepare_message(self):
		msgs = []
		for rec_group in self.recipients:
			msg = EmailMessage()
			msg['From'] = self.frm
			msg['To'] = rec_group
			content = self.content
			msg['Subject'] = content['meta']['subject'][0]
			msg.set_content(content['raw'])
			msg.add_alternative(content['html'], subtype='html')
			msgs.append(msg)
		return msgs

	def _read_recipients_from_file(self, filename):
		mail = "[^@]+@[^@]+\.[^@]+"
		rec = []

		if isinstance(filename, list):
			for file in filename:
				if re.match(mail, file):
					rec.append(file)
				else:
					with open(file) as f:
						rec += list(line.rstrip('\n') for line in f)
		else:
			raise ValueError("Recipients may be list of files or mails")

		return list(chunks(rec, self._limit))

	@staticmethod
	def _read_markdown_body(filename):
		with open(filename) as f:
			text1 = f.read()

		md = Markdown(extensions=['markdown.extensions.meta'])
		text2 = md.convert(text1)

		return {'raw': text1, 'html': text2, 'meta': md.Meta}


def mail_wrapper(args):
	mail = Mail(args.login, args.frm,
	            recipients=[args.recipients],
	            body=args.inputs,
	            server=args.server)
	mail.send()


if __name__ == "__main__":
	pass
