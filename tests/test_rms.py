#!/usr/bin/env python3

import os
import unittest
from byro.rms import RMS


class RmsTest(unittest.TestCase):

	def test_init(self):
		pass

	def test_get_marks(self):
		file_lists = {
			'simple':   (['1-abc', '2-abc', '3-abc'],       [1, 2, 3]),
			'duplicity':(['1-abc', '2-abc', '2-abc'],       [1, 2, 2]),
			'zerofill': (['001-abc', '002-abc', '003-abc'], [1, 2, 3])
		}
		rms = RMS()
		for key, val in file_lists.items():
			input_list=val[0]
			expected=val[1]
			with self.subTest(input_list=input_list, expected=expected, rms=rms):
				returned = rms.get_marks(input_list)
				self.assertEqual(returned, expected)

	def test_last_sign_mark(self):
		pass

	def test_new_sign_mark(self):
		pass