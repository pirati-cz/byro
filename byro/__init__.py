#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Bureaucracy assistant.

From open source components create tool for every office work:

* ocr
* pdf prepared from markdown
* integration with git repository
* mass mail
* preparation of vycetka

Basically it is only a wrapper over some handy open source tools like Pandoc, Tesseract, git, Redmine API and LaTeX.
"""

__version__ = "0.5.8"
__status__ = "Alpha"
__license__ = "Affero GNU-GPL v3"
__author__ = "Ondřej Profant, Jakub Michálek"
__credits__ = ["Ondřej Profant", "Jakub Michálek"]
__copyright__ = "Copyright 2015, Ondřej Profant, Jakub Michálek"
__maintainer__ = "Ondřej Profant"
__email__ = "ondrej.profant@gmal.com"

__all__ = ["bredmine", "configargparse", "mail", "pandoc", "sign", "utils", "vycetka", "converter"]
