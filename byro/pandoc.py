# date:                   \today{}
# abstract:               Lorem ipsum
# fontsize:               10
# geometry:               margin=2cm
# lang:                   cs
# mainlang:               czech
import os
import sys
import subprocess
from byro.utils import Utils


class Pandoc:
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
            return Utils.split_filename(input)[0] + ".pdf"
        else:
            return output

    def convert(self, input, template="", output=None, verbosity=True):
        output = Pandoc.output_name(input, output)

        command = [self.bin] + \
                  self.params + \
                  ["-f", "markdown",
                   "--latex-engine=xelatex",
                   "-t", "latex"]

        if template:
            # todo
            pass

        command += ["-o", output, input]

        subprocess.call(command)

        if verbosity:
            print("%s byl konvertován v %s" % (input, output))
