#!/usr/bin/env python3

from distutils.core import setup

setup(name='Byro',
    version='0.1.0',
    description='',
    license='Affero GNU-GPL',
    author='Ondřej Profant, Jakub Michálek',
    author_email='ondrej.profant@gmal.com',
    url='https://github.com/pirati-cz/byro/',
    libraries=['wget', 'dateutils', 'markdown', 'ConfigArgParse', 'python-redmine', 'python-docx'],
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
