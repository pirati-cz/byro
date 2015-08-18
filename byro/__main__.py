#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
See __init__.py.__doc__
"""

import sys
import locale
import shutil
from os import path
from byro.vycetka import vycetka_wrapper
from byro.sign import PdfSign
from byro.convertor import Convertor
from byro.configargparse import ByroParse
from byro.mail import mail_wrapper
from byro.utils import (ocr, save)
from byro import (__author__)

__dir__ = path.realpath(path.dirname(__file__))


class App:
	def __init__(self):
		self.arg_parser = None
		self.args = None
		self.user_confg = path.join(path.expanduser('~'), ".byro.ini")
		self.default_config = path.join(__dir__, 'resource', 'config-example.ini')

	def _first_run(self):
		if not path.exists(self.user_confg):
			print("First run, create user config: ", self.user_confg)
			shutil.copy(self.default_config, self.user_confg)

		nautilus_scripts = path.expanduser('~') + "/local/share/nautilus/scripts"
		if sys.platform == "linux2" and path.exists(nautilus_scripts):
			print("Would you like install Nautilus scripts?")
			print("Unfortunetly not implemented yet")
		# TODO

	def _parse_args(self):

		subcommands = ["pdf", "sign", "vycetka", "save", "mail", "ds", "ocr", "args"]

		p = ByroParse(
			subcommands,
			default_config_files=[self.default_config, self.user_confg],
			description=__doc__,
			epilog=str(__author__)
		)

		p.add('-c', '--config', is_config_file=True, help='config file path')
		p.add('-g', '--gui', type=bool, help="")
		p.add('-l', '--locale', help="")
		p.add('-o', '--out', help="Output file name")

		vyc = p.add_argument_group('Vycetka', "Generates \"vycetka\" for Prague City Hall.")
		vyc.add('--url', help="Target Redmine url.")
		vyc.add('-p', '--project', help="Redmine project name.")
		vyc.add('-y', '--year',  help="Values: this, last, 2014, 2015, ...")
		vyc.add('-m', '--month', help="Values: this, last, leden, únor, ..., prosinec, 1, ..., 12. Determinate by localization.")
		vyc.add('-u', '--user',  help="Redmine user nickname or id.")

		sign = p.add_argument_group('Sign', "Digital sign of pdf file.")
		sign.add('-k', '--sign-key', help="Path to the key.pfx")
		sign.add('--sign-bin', help="Path to the jPdfSign")
		sign.add('-V', '--sign-visible', type=bool, help="")
		sign.add('--sign-reason', help="")
		sign.add('--sign-location', help="")
		sign.add('--sign-contact', help="")

		pdf = p.add_argument_group('Pdf', "Convert markdown into pdf via Pandoc.")
		pdf.add('--pandoc-bin', help="Path to pandoc binary.")
		pdf.add('--tex-bin', help="")
		pdf.add('-t', '--template', help="Path to XeLaTeX template.")

		mail = p.add_argument_group('Mail', "Send mass mails, body is markdown file, list of recipients is file")
		mail.add("-r", "--recipients", help="Email, or path to text file with recipients divided by newline.")
		mail.add("-f", "--frm", help="Sender email address.")
		mail.add("--login", help="Email login")
		mail.add("--server", help="Email server")
		mail.add("--port", help="Port")

		ocr = p.add_argument_group("ocr", "OCR images: byro -o <text>.txt file1.jpg file2.jpg")

		ds = p.add_argument_group('Ds')
		ds.add('--ds-id', help="")

		p.add_argument('inputs', metavar='input files', nargs='*', help='Input files')

		self.arg_parser = p
		self.args = p.parse_args()

	def _before_run(self):
		self._first_run()
		locale.setlocale(locale.LC_ALL, self.args.locale)

	def pdf(self):
		convertor = Convertor(self.args.pandoc_bin)
		convertor.convert(self.args.inputs)

	def vycetka(self):
		vycetka_wrapper(self.args)

	def sign(self):
		sign = PdfSign(self.args.sign_bin, self.args.sign_key)
		sign.sign(self.args.inputs)

	def mail(self):
		mail_wrapper(self.args)

	def save(self):
		save()

	def ocr(self):
		text=ocr(self.args.inputs, self.args.out)
		if not self.args.out:
			print(text)

	def args_test(self):
		print(self.args)

	def main(self):

		self._parse_args()

		self._before_run()

		c = self.args.command

		if c == 'args':
			self.args_test()
		elif c == "pdf":
			self.pdf()
		elif c == "ocr":
			self.ocr()
		elif c == "sign":
			self.sign()
		elif c == "mail":
			self.mail()
		elif c == "save":
			self.save()
		elif c == "vycetka":
			self.vycetka()
		else:
			self.arg_parser.print_help()


def main():
	return App().main()


if __name__ == "__main__":
	sys.exit(main())
