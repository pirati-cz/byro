import os
import sys
import subprocess
from byro.utils import Utils

_pandoc_can_convert = [".md", ".mkd"]
_lo_can_convert = [".docx", ".doc", ".xls", ".xlsx", ".odt", ".odp"]


class ValueErrorLO(ValueError):
    """
    File extensions that cannot be converted by Pandoc,
    byt LibreOffice can do the job.
    """
    pass


class ValueErrorPdf(ValueError):
    pass


class Convertor:
    def __init__(self, bin="pandoc"):
        self.bin = bin
        self.params = ["--smart"]
        self.check_dependency()

    def check_dependency(self):
        command = [self.bin, "-v"]
        fnull = open(os.devnull, 'w')

        try:
            subprocess.check_call(command, stdout=fnull)
        except subprocess.CalledProcessError:
            print("Cesta k pandoc není správná. Cesta: %s" % command, file=sys.stderr)
            exit()
        finally:
            fnull.close()

    @staticmethod
    def output_name(input, output = None):
        if output is None:
            splited = Utils.split_filename(input[0])
            if splited[1] in _lo_can_convert:
                raise ValueErrorLO()
            elif splited[1] == ".pdf":
                raise ValueErrorPdf("Input file already is PDF")
            return splited[0] + ".pdf"
        else:
            return output

    def convert(self, input, template="", output=None, verbosity=True):

        for file in input:
            if not os.path.exists(file):
                raise ValueError("File %s does not exists" % file)

        try:
            output = Convertor.output_name(input, output)

            command = [self.bin] + \
                      self.params + \
                      ["-f", "markdown",
                       "--latex-engine=xelatex",
                       "-t", "latex"]

            if template:
                # todo
                pass

            command += ["-o", output] + input

            subprocess.call(command)

            if verbosity:
                print("%s byl konvertován v %s" % (input, output))

        except ValueErrorLO:
            self.convertDocx(input)

    def convertDocx(self, input, verbosity=True):
        if not os.path.exists(input):
            raise ValueError("File %s does not exist" % input)

        command = ['libreoffice', '--invisible', '--convert-to', 'pdf',]
        subprocess.call(command)

        if verbosity:
                print("%s byl konvertován do PDF." % (input))
