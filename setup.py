#!/usr/bin/env python3

from distutils.core import setup

setup(name='Byro',
    version='0.3',
    description='',
    license='Affero GNU-GPL',
    author='Ondřej Profant, Jakub Michálek',
    author_email='ondrej.profant@gma.com',
    url='https://github.com/pirati-cz/byro/',
    libraries=['python-docx', 'ConfigArgParse', 'MarkupSafe'],
    classifiers = [
        'Intended Audience :: Users',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        ]
    )
