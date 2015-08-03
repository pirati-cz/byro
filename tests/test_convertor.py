import os
import unittest
from byro.convertor import (Convertor, ValueErrorLO, ValueErrorPdf)


def get_test_files_dir():
        return os.path.realpath(os.path.dirname(__file__)) + "/data/"


class Convert(unittest.TestCase):

    def test_convertor_input_name(self):
        names = ["main.md"]
        returned = Convertor.output_name(names)
        expected = "main.pdf"
        self.assertEqual(returned, expected)

    def test_convertor_docx_name(self):
        names = ["main.docx"]
        with self.assertRaises(ValueErrorLO):
            returned = Convertor.output_name(names)

    def test_convertor_pdf_name(self):
        names = ["main.pdf"]
        with self.assertRaises(ValueErrorPdf):
            returned = Convertor.output_name(names)

    def test_convertor_convert(self):
        pandoc = Convertor()
        path = get_test_files_dir()
        filename = [path + 'simple-body.md']
        expected = path + 'simple-body.pdf'
        pandoc.convert(filename, verbosity=False)
        self.assertTrue(os.path.exists(expected))
        os.remove(expected)
