#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
See __init__.py.__doc__
"""

import re
import sys
import locale
import shutil
from os import path
from byro.vycetka import vycetka_wrapper
from byro.sign import PdfSign
from byro.converter import Converter
from byro.configargparse import ByroParse
from byro.mail import mail_wrapper
from byro.utils import (ocr as ocr_wrapper, save as save_wrapper)
from byro import (__author__, __version__)

__dir__ = path.realpath(path.dirname(__file__))


class App:

	def __init__(self, arguments):
		self.raw_argv = arguments
		self.arg_parser = None
		self.args = None
		self.configs = {
			'default':  path.join(__dir__, 'resource', 'config-example.ini'),
			'user':     path.join(path.expanduser('~'), '.byro.ini')
		}
		self._parse_args()

	def _first_run(self):
		if not path.exists(self.configs['user']):
			print("First run, create user config: ", self.configs['user'])
			shutil.copy(self.configs['default'], self.configs['user'])

		nautilus_scripts = path.expanduser('~') + "/local/share/nautilus/scripts"
		if sys.platform == "linux2" and path.exists(nautilus_scripts):
			print("Would you like install Nautilus scripts?")
			print("Unfortunetly not implemented yet")
		# TODO

	def _parse_args(self):

		subcommands = ["pdf", "sign", "vycetka", "save", "mail", "ds", "ocr", "arg", "config", "version"]
		configs = list(self.configs.values())

		p = ByroParse(
			subcommands,
			default_config_files=configs,
			description=__doc__,
			epilog="Version: " + __version__ + ", Authors: " + str(__author__)
		)

		p.add('-c', '--config', is_config_file=True, help='config file path')
		p.add('-g', '--gui', type=bool, help="")
		p.add('-l', '--locale', help="Locale, for example: cs_CZ, en_US")
		p.add('-o', '--out', help="Output file name")
		# TODO: config path

		con = p.add_argument_group('Config', "Show config path and ends.")
		con.add('-a', '--add', help="Add argument into used config")

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
		# TODO
		pdf.add('-D', '--print-default-template', help="Print default template.")

		mail = p.add_argument_group('Mail', "Send mass mails, body is markdown file, list of recipients is file")
		mail.add("-r", "--recipients", help="Email, or path to text file with recipients divided by newline.")
		mail.add("-f", "--frm", help="Sender email address.")
		mail.add("--login", help="Email login")
		mail.add("--server", help="Email server")
		mail.add("--port", help="Port")

		ocr = p.add_argument_group("Ocr", "OCR images: byro -o <text>.txt file1.jpg file2.jpg")

		ds = p.add_argument_group('Ds')
		ds.add('--ds-id', help="")

		p.add_argument('inputs', metavar='input files', nargs='*', help='Input files')

		self.arg_parser = p
		self.args = p.parse_args(self.raw_argv)

	def _before_run(self):
		self._first_run()
		try:
			locale.setlocale(locale.LC_ALL, self.args.locale)
		except locale.Error:
			# Ubuntu specific error
			# Issue: https://github.com/pirati-cz/byro/issues/17
			error_mes = """
Váš OS neobsahuje správné locale.
Zkuste je vygenerovat příkaz:
sudo locale-gen %s
			""" % self.args.locale
			print(error_mes, file=sys.stderr)
			exit()

	def config(self):
		if self.args.add:
			pattern = '([\w-]*)=(\w*)'
			m = re.match(pattern, self.args.add)
			if m:
				g = m.groups()
				#TODO
				print('replace', g[0], 'with', g[1])
				#command = ["re.sub('^# deb', 'deb', line)"]
				#with open(self.configs['user'], "r") as sources:
				#	for line in sources.readlines():
				#		print(line)
			else:
				print('Unknown format:', self.args.add)
		else:
			print('Configs:')
			print(self.configs)
			print('Arguments:')
			print(self.args)

	def pdf(self):
		converter_wrapper(self.args)

	def vycetka(self):
		vycetka_wrapper(self.args)

	def sign(self):
		sign = PdfSign(self.args.sign_bin, self.args.sign_key)
		sign.sign(self.args.inputs)

	def mail(self):
		mail_wrapper(self.args)

	@staticmethod
	def save():
		save_wrapper()

	def ocr(self):
		locale = self.args.locale
		if locale in ('eng', 'ces'):
			lang = locale
		elif locale == 'en_US':
			lang = 'eng'
		elif locale == 'cs_CZ':
			lang = 'ces'
		else:
			raise Exception("Unknown locale")

		text = ocr_wrapper(self.args.inputs, self.args.out, lang)
		if not self.args.out:
			print(text)

	@staticmethod
	def version():
		print(__version__)

	def args_test(self):
		print(self.args)

	def main(self):

		self._before_run()

		c = self.args.command

		if c == 'arg':
			self.args_test()
		elif c == "config":
			self.config()
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
		elif c == "version":
			self.version()
		else:
			self.arg_parser.print_help()


def main():
	arguments = sys.argv[1:]
	app = App(arguments)
	return app.main()


if __name__ == "__main__":
	sys.exit(main())
