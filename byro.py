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
        p.add('-g', '--gui', type=bool, help="")
        p.add('-l', '--locale',   help="")

        vyc = p.add_argument_group('Vycetka', "Generates \"vycetka\" for Prague City Hall.")
        vyc.add(      '--url',      help="Target Redmine url.")
        vyc.add('-p', '--project',  help="Redmine project")
        vyc.add('-y', '--year',     help="Year")
        vyc.add('-m', '--month',    help="Month")
        vyc.add('-u', '--user',     help="Redmine user nickname or id")

        sign = p.add_argument_group('Sign', "Digital sign of pdf file.")
        sign.add('-k', '--sign-key', help="Path to the key.pfx")
        sign.add(	    '--sign-bin', help="Path to the jPdfSign" )
        sign.add('-V', '--sign-visible', type=bool, help="")
        sign.add(	    '--sign-reason', help="" )
        sign.add(	    '--sign-location', help="" )
        sign.add(	    '--sign-contact', help="" )

        pdf = p.add_argument_group('Pdf', "Convert markdown into pdf via Pandoc.")
        pdf.add(      '--pandoc-bin', help="")
        pdf.add(      '--tex-bin', help="")
        pdf.add('-t', '--template', help="")
        pdf.add('-i', '--input',    help="Input file name")
        pdf.add('-o', '--out',      help="Output file name")

        mail = p.add_argument_group('Mail', "Send mass mails, body is markdown file, list of recipients is file")

        ds = p.add_argument_group('Ds')
        ds.add(      '--ds-id', help="")

        self.arg_parser = p
        self.args = p.parse_args()

    def _before_run(self):
        locale.setlocale(locale.LC_ALL, self.args.locale)

    def pdf(self):
        pandoc = Pandoc(self.args.pandoc_bin)
        #TODO: gives real filename
        pandoc.convert(self.args.input)

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
