#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import locale
from byro.bredmine import BRedmine
from byro.vycetka import (Cmd, DocX)
from byro.sign import PdfSign
from byro.pandoc import Pandoc
from byro.configargparse import ByroParse


class App:

    def __init__(self):
        self.arg_parser = None
        self.args = None

    def _parse_args(self):

        subcommands = ["pdf", "sign", "vycetka", "save", "mail", "ds", "args"]

        p = ByroParse(
            subcommands,
            default_config_files=['files/config.ini']
        )

        p.add('-c', '--config', is_config_file=True,  help='config file path')
        p.add(      '--url',      help="Target Redmine url.")
        p.add('-p', '--project',  help="Redmine project")
        p.add('-y', '--year',     help="")
        p.add('-m', '--month',    help="")
        p.add('-u', '--user',     help="Redmine user nickname or id")
        p.add('-i', '--input',    help="Input file name")
        p.add('-o', '--out',      help="Output file name")
        p.add('-l', '--locale',   help="")
        p.add('-g', '--gui', type=bool, help="")
        p.add('-k', '--sign-key', help="")
        p.add(	    '--sign-bin', help="" )
        p.add('-V', '--sign-visible', type=bool, help="")
        p.add(	    '--sign-reason', help="" )
        p.add(	    '--sign-location', help="" )
        p.add(	    '--sign-contact', help="" )
        p.add(      '--pandoc-bin', help="")
        p.add(      '--tex-bin', help="")
        p.add(      '--ds-id', help="")

        self.arg_parser = p
        self.args = p.parse_args()

    def _before_run(self):
        locale.setlocale(locale.LC_ALL, self.args.locale)

    def pdf(self):
        pandoc = Pandoc(self.args.pandoc_bin)
        #TODO: gives real filename
        pandoc.convert("README.md")

    def vycetka(self):
        redmine = BRedmine(self.args.user, self.args.url, self.args.project, self.args.month)
        data = redmine.get_data()
        # data.export_to_bin_file("data-6-OP.p")
        docx = DocX(data, self.args.out)
        docx.show()

    def sign(self):
        pass
        sign = PdfSign(self.args)
        sign.sign(self.args.input)

    def args_test(self):
        print(self.args)

    def main(self):

        self._parse_args()

        self._before_run()

        c = self.args.command

        if c == 'args':
            self.args_test()
        elif c == "pdf":
            self.pdf()
        elif c == "sign":
            self.sign()
        elif c == "vycetka":
            self.vycetka()
        else:
            self.arg_parser.print_help()

if __name__ == "__main__":
    App().main()
