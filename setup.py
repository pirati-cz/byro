#!/usr/bin/env python3

from setuptools import (setup, find_packages)

setup(
    # Basic
    name='Byro',
    version='0.2.0',
    packages=find_packages(),
    scripts=['byro.py'],

    # Requirements
    install_requires= ["wget", "dateutils", "markdown",
                       "ConfigArgParse",
                       "python-redmine", "python-docx",
                       "pytesseract"],

    # About
    author='Ondřej Profant, Jakub Michálek',
    author_email='ondrej.profant@gmal.com',
    description='',
    license='Affero GNU-GPL v3',
    keywords="bureaucracy administration ocr pdf markdown",
    url='https://github.com/pirati-cz/byro/',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Users',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Natural Language :: Czech',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Office/Business',
        'Topic :: Utilities'
        ]
    )
