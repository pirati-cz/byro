import os
import unittest
from byro.sign import PdfSign

bin = "/opt/jsignpdf/JSignPdf.jar"
key = ""


def get_test_files_dir():
        return os.path.realpath(os.path.dirname(__file__)) + "/data/"


def test_dependency():
    return not (os.path.exists(bin) and os.path.exists(key))


@unittest.skipIf(test_dependency(), "PdfSign bin or Sign key not found.")
class Sign(unittest.TestCase):

    def test_sign(self):

        sign = PdfSign(bin, key)
        path = get_test_files_dir() + "advance-body.pdf"
        sign.sign(path)
        expexted = get_test_files_dir() + "advance-body_signed.pdf"
        self.assertTrue(os.path.exists(expexted))
        self.assertTrue(False)