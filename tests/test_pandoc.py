import os
import unittest
from byro.pandoc import Pandoc


def get_test_files_dir():
        return os.path.realpath(os.path.dirname(__file__)) + "/data/"


class Convert(unittest.TestCase):

    def test_name(self):
        name = "main.md"
        returned = Pandoc.output_name(name)
        expected = "main.pdf"
        self.assertEqual(returned, expected)

    def test1(self):
        pandoc = Pandoc()
        path = get_test_files_dir()
        filename = path + 'simple-body.md'
        expected = path + 'simple-body.pdf'
        pandoc.convert(filename, verbosity=False)
        self.assertTrue(os.path.exists(expected))
        os.remove(expected)
