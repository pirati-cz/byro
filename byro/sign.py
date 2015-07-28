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

    def __init__(self, args):
        self.bin = ["java", "-jar", args.sign_bin]
        self.key = args.sign_key
        self.reason = args.sign_reason
        self.check_dependency()

    def download_dependency(self):
        url = "http://sourceforge.net/projects/jsignpdf/files/latest/download?source=files"
        file = "jsign.zip"
        wdir = "tmp"
        try:
            os.mkdir(wdir)
            os.chdir(wdir)
            print("Download lib.")
            wget.download(url, out=file)
            zip = zipfile.ZipFile(file=file,mode='r')
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
            print("Cesta k JsignPdf není správná. Cesta: %s" % command, file=sys.stderr)
            exit()

        if not os.path.isfile(self.key):
            print("Cesta k podpisovému klíči není správná. Cesta: %s" % self.key, file=sys.stderr)
            exit()

    def sign(self, filename):

        command = self.bin + ["-kst", "PKCS12", "-ksf", self.key, "-V", filename]
        passwd = getpass.getpass()
        command[:-1] += ["-ksp", passwd]

        try:
            subprocess.call(command)
        except Exception as e:
            print(e)
        finally:
            del(passwd, command)
