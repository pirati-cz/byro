#!/usr/bin/env python3

import os
import unittest
from byro.utils import ocr


def get_test_files_dir():
	return os.path.join(os.path.realpath(os.path.dirname(__file__)), "data")


class Ocr(unittest.TestCase):
	def test_en(self):
		file = os.path.join(get_test_files_dir(), 'ocr-test-en.jpg')
		text = ocr([file], None, "en")

	@unittest.skip
	def test_en_multi(self):
		file = os.path.join(get_test_files_dir(), 'ocr-test-en.jpg')
		ocr([file, file], None, "en")

	@unittest.skip
	def test_cs(self):
		file = os.path.join(get_test_files_dir(), 'ocr-test-cs.png')
		ocr([file])
