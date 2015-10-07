import os
import sys
import subprocess
from byro.utils import Utils

_pandoc_can_convert = [".md", ".mkd"]
_lo_can_convert = [".docx", ".doc", ".xls", ".xlsx", ".odt", ".odp"]
__dir__ = os.path.realpath(os.path.dirname(__file__))


class ValueErrorLO(ValueError):
	"""
	File extensions that cannot be converted by Pandoc,
	byt LibreOffice can do the job.
	"""
	pass


class ValueErrorPdf(ValueError):
	pass


class Converter:
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
			splitted = Utils.split_filename(input[0])
			if splitted[1] in _lo_can_convert:
				raise ValueErrorLO()
			elif splitted[1] == ".pdf":
				raise ValueErrorPdf("Input file already is PDF")
			return splitted[0] + ".pdf"
		else:
			return output

	@staticmethod
	def _prepare_inputs(inputs):
		for i in range(len(inputs)):
			if not os.path.exists(inputs[i]):
				raise ValueError("File %s does not exists" % inputs[i])
			inputs[i] = os.path.realpath(inputs[i])

	def _prepare_command(self, inputs, template="", output=None):
		"""
		:param inputs: list of input files
		:param template: path to template or template name (from prepared templates)
		:param output: output file name
		:return: command splitted into list
		"""
		output = os.path.realpath(Converter.output_name(inputs, output))

		command = [self.bin] + \
					self.params + \
					["-f", "markdown",
					"-t", "latex",
					"-o", output,
					"--latex-engine=xelatex"]

		if template:
			if template == 'none':
				pass  # default template
			elif template == 'letter':
				# for named template is necessary to change working directory
				template = "--template=letter/main.tex"
				command.append(template)
			elif template == 'brochure':
				raise NotImplementedError
			elif os.path.exists(template):
				command.append("--template=" + template)

		command += inputs

		return command

	def convert(self, inputs, template="", output=None, verbosity=True):

		self._prepare_inputs(inputs)

		try:
			command = self._prepare_command(inputs, template, output)

			old_dir = os.curdir
			if template:
				styles_dir = os.path.join(__dir__, 'resource', "styles")
				os.chdir(styles_dir)

			subprocess.call(command)

			if template:
				os.chdir(old_dir)

			if verbosity:
				print("%s byl konvertován v %s" % (inputs, output))

		except ValueErrorLO:
			self.convertDocx(inputs)

		# ~/.cabal/bin/pandoc -f markdown -t latex --latex-engine=xelatex --template=template.tex -o text.pdf -V my_var=xedf text.md
		#

	def convertDocx(self, inputs, verbosity=True):

		command = ['libreoffice', '--invisible', '--convert-to', 'pdf'] + inputs
		subprocess.call(command)

		if verbosity:
			print("%s byl konvertován do PDF." % str(inputs))
