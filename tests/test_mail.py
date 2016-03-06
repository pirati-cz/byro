#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import unittest
from os.path import join, realpath, dirname
from byro.mail import Mail


def get_test_files_dir():
    return join(realpath(dirname(__file__)), "data", "mail")


class Recipients(unittest.TestCase):

    def test_recipients_mail(self):
        body = [join(get_test_files_dir(), "simple-body.md")]
        mail = ["john.doe@example.com"]
        m = Mail("", "", body=body, recipients=mail)
        expected = [mail]
        self.assertEqual(m.recipients, expected)

    def test_recipients_file(self):
        filename = join(get_test_files_dir(), "recipients.txt")
        body = [join(get_test_files_dir(), "simple-body.md")]
        m = Mail("", "", body=body, recipients=[filename], limit=2)
        expected = [["email@example.com", "email@example.cz"], ["email@example.eu"]]
        self.assertEqual(m.recipients, expected)


class Body(unittest.TestCase):

    def test_mail_body_simple(self):
        path = get_test_files_dir()
        filename = join(path, "simple-body.md")
        returned = Mail._read_markdown_body(filename)

        expected = 'Dobrý den,\n\ndovoluji se Vás oslovit ve věci mimořádné důležitosti.'
        self.assertEqual(returned['raw'], expected)

        expected = '<p>Dobrý den,</p>\n<p>dovoluji se Vás oslovit ve věci mimořádné důležitosti.</p>'
        self.assertEqual(returned['html'], expected)

        self.assertEqual(returned['meta'], {})

    def test_mail_body_advance(self):
        path = get_test_files_dir()
        filename = join(path, "advance-body.md")
        returned = Mail._read_markdown_body(filename)

        expected = "---\nSubject: Hello world!\n---\n\n\nHello world\n===========\n\n**bold**\n\n*italic*\n\n[some link](www.example.com)"
        self.assertEqual(returned['raw'], expected)
