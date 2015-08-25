#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
from setuptools import (setup, find_packages)
from byro import (__version__, __author__, __email__, __license__, __doc__)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

setup(
	# Basic
	name='Byro',
	version=__version__,
	packages=find_packages(),
	# Entry ponit
	entry_points={
		'console_scripts': [
			'byro = byro.__main__:main',
		]
	},

	# Requirements
	install_requires=["wget", "dateutils", "markdown",
		"ConfigArgParse", "sh",
		"python-redmine", "python-docx",
		"pytesseract"],

	package_data={
		'byro': ['resource/*']
	},

	# About
	author=str(__author__),
	author_email=__email__,
	description='Bureaucracy assistant',
	license=__license__,
	long_description=__doc__,
	keywords="bureaucracy administration pdf git ocr markdown",
	url='https://github.com/pirati-cz/byro/',

	classifiers=[
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
