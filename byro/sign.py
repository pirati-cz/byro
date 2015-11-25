#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import sys
import wget
import shutil
import os.path
import zipfile
import getpass
import subprocess


class PdfSign:
	def __init__(self, bin, key):
		self.bin = ["java", "-jar", bin]
		self.key = key
		self.reason = ""
		self.check_dependency()
		self.errors = {
			'key': "Cesta k podpisovému klíči není správná. Definujete jí parametrem -k <cesta>. Zadaná cesta: %s",
			'bin': "Cesta k JsignPdf není správná. Cesta: %s"
		}

	@staticmethod
	def download_dependency():
		# todo
		url = "http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files"
		file = "jsign.zip"
		wdir = "tmp"
		try:
			os.mkdir(wdir)
			os.chdir(wdir)
			print("Download lib.")
			wget.download(url, out=file)
			zip = zipfile.ZipFile(file=file, mode='r')
			zip.extractall()
			dist_file = "jsignpdf-1.6.1"
			if os.path.isfile(dist_file):
				os.rename(src=dist_file, dst="../lib/jsign")
			else:
				print("", file=sys.stderr)
		except:
			print("", file=sys.stderr)
		finally:
			os.chdir("..")
			shutil.rmtree(wdir, ignore_errors=True)

	def check_dependency(self):
		command = self.bin + ["-v"]

		try:
			subprocess.check_call(command)
		except subprocess.CalledProcessError:
			print(self.errors['bin'] % command, file=sys.stderr)
			exit()

		try:
			if not os.path.isfile(self.key):
				raise FileExistsError
		except (TypeError, FileExistsError):
			print(self.errors['key'] % self.key, file=sys.stderr)
			exit()

	def sign(self, filenames):
		passwd = getpass.getpass()
		command = self.bin + ["-kst", "PKCS12", "-ksf", self.key, "-V", "-ksp", passwd]

		for filename in filenames:
			try:
				subprocess.call(command + [filename])
			except Exception as e:
				print(e)

		del (passwd, command)


if __name__ == "__main__":
	pass