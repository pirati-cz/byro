# date:                   \today{}
# abstract:               Lorem ipsum
# fontsize:               10
# geometry:               margin=2cm
# lang:                   cs
# mainlang:               czech
import sys
import subprocess
from byro.utils import Utils


class Pandoc:
    def __init__(self, bin):
        self.bin = bin
        self.params = ["--smart"]
        self.check_dependency()

    def check_dependency(self):
        command = [self.bin, "-v"]

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print("Cesta k pandoc není správná. Cesta: %s" % command, file=sys.stderr)
            exit()

    def convert(self, input, template=None, output=None):
        if output is None:
            output = Utils.split_filename(input)[0] + ".pdf"
        template = None
        command = [self.bin] + \
                  self.params + \
                  ["-f", "markdown",
                   "--latex-engine=xelatex",
                   "-t", "latex",
                   "-o", output, input]

        subprocess.call(command)
