import os
from os.path import join, exists, realpath, dirname
import unittest
from byro.converter import (Converter, ValueErrorLO, ValueErrorPdf)


def get_test_files_dir():
	return join(realpath(dirname(__file__)), "data", "mail")


class Convert(unittest.TestCase):

	def test_converter_input_name(self):
		names = ["main.md"]
		returned = Converter.output_name(names)
		expected = "main.pdf"
		self.assertEqual(returned, expected)

	def test_converter_docx_name(self):
		names = ["main.docx"]
		with self.assertRaises(ValueErrorLO):
			returned = Converter.output_name(names)

	def test_converter_pdf_name(self):
		names = ["main.pdf"]
		with self.assertRaises(ValueErrorPdf):
			returned = Converter.output_name(names)

	def test_prepare_command_1(self):
		converter = Converter("pandoc")
		returned = converter._prepare_command(["meta.md", "text.md"], "/tmp/letter2.tex", "text.pdf")
		expected = ["pandoc", "--smart", "-f", "markdown", "-t", "latex", "-o",
		            realpath("text.pdf"), "--latex-engine=xelatex", "meta.md", "text.md"]
		self.assertEqual(returned, expected)

	def test_prepare_command_2(self):
		converter = Converter("pandoc")
		returned = converter._prepare_command(["meta.md", "text.md"], "/tmp/letter2.tex")
		expected = ["pandoc", "--smart", "-f", "markdown", "-t", "latex", "-o",
					realpath("meta.pdf"), "--latex-engine=xelatex", "meta.md", "text.md"]
		self.assertEqual(returned, expected)

	def test_converter_convert(self):
		converter = Converter("pandoc")
		path = get_test_files_dir()
		filename = [join(path, 'simple-body.md')]
		expected = join(path, 'simple-body.pdf')
		converter.convert(filename, verbosity=False)
		self.assertTrue(exists(expected))
		os.remove(expected)
