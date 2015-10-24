#!/usr/bin/env python3

import os
import re
import sh
# from sh import git


class RMS:
	"""Record management system

	Very simple RMS based on directory structure versioned by git CVS.
	"""

	def __init__(self, directory='.'):
		self.directory = directory
		# TODO check if directory is git
		# git status

	def get_marks(self, files=None):
		"""Get all used marks in given RMS (directory)"""
		if not files:
			files = os.listdir(self.directory)

		nums = []
		pattern = '([0-9]*)-\w*'
		for n in files:
			m = re.match(pattern, n)
			if m:
				nums.append(int(m.groups()[0]))
		nums.sort()
		return nums

	def last_sign_mark(self):
		"""
		Returns last sign mark (spisová značka)
		"""
		nums = self.get_marks()

		if not nums:
			return 0

		return nums[-1]

	def new_sign_mark(self, name="", text=""):
		"""
		Find and create new sign mark
		"""
		old_dir = os.curdir()
		os.chdir(self.directory)

		sh.git("pull")
		mark = self.last_sign_mark() + 1

		new_dir = str(mark).zfill(3) + '-' + name
		readme = os.path.join(new_dir, 'readme.md')

		os.mkdir(new_dir)

		with open(readme, "w") as file:
			file.write('# Spis ' + mark + name)
			file.write(text)

		sh.git("add", readme)
		sh.git("push")

		os.chdir(old_dir)

	def search_in_file(self):
		pass
