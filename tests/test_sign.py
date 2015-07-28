import os
import unittest
from byro.sign import PdfSign


class Args:
    sign_bin = "/opt/jsignpdf/JSignPdf.jar"

    def __init__(self):
        self.sign_key = ""
        self.sign_reason = ""

    @staticmethod
    def exists():
        return os.path.exists(Args.sign_bin)


@unittest.skipIf(not Args.exists(), "Nenalezena binárka pdfSign")
class SignTest(unittest.TestCase):

    def sign_test(self):
        sign = PdfSign(Args)
        sign.sign()
        pass