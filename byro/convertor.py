import os
import sys
import subprocess
from byro.utils import Utils

_pandoc_can_convert = [".md", ".mkd"]
_lo_can_convert = [".docx", ".doc", ".xls", ".xlsx", ".odt", ".odp"]


class ValueErrorLO(ValueError):
	"""
	File extensions that cannot be converted by Pandoc,
	byt LibreOffice can do the job.
	"""
	pass


class ValueErrorPdf(ValueError):
	pass


class Convertor:

	def __init__(self, bin):
		self.bin = bin
		self.params = ["--smart"]
		self.check_dependency()

	def check_dependency(self):
		command = [self.bin, "-v"]

		try:
			with open(os.devnull, 'w') as fnull:
				subprocess.check_call(command, stdout=fnull)
		except subprocess.CalledProcessError:
			print("Cesta k pandoc není správná. Cesta: %s" % command, file=sys.stderr)
			exit()

	@staticmethod
	def output_name(input, output=None):
		if output is None:
			splited = Utils.split_filename(input[0])
			if splited[1] in _lo_can_convert:
				raise ValueErrorLO()
			elif splited[1] == ".pdf":
				raise ValueErrorPdf("Input file already is PDF")
			return splited[0] + ".pdf"
		else:
			return output

	def convert(self, inputs, template="", output=None, verbosity=True):

		for file in inputs:
			if not os.path.exists(file):
				raise ValueError("File %s does not exists" % file)

		try:
			output = Convertor.output_name(inputs, output)

			command = [self.bin] + \
					  self.params + \
					  ["-f", "markdown",
					   "--latex-engine=xelatex",
					   "-t", "latex"]

			if template:
				command.append("--template=" + template)
				print("pridano")

			command += ["-o", output] + inputs

			subprocess.call(command)

			if verbosity:
				print("%s byl konvertován v %s" % (inputs, output))

		except ValueErrorLO:
			self.convertDocx(inputs)

	def convertDocx(self, inputs, verbosity=True):

		command = ['libreoffice', '--invisible', '--convert-to', 'pdf'] + inputs
		subprocess.call(command)

		if verbosity:
			print("%s byl konvertován do PDF." % str(inputs))
