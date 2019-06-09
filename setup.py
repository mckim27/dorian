#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************
# @FILE       setup.py

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import sys
from setuptools import find_packages, setup
from coverage import __version__, __author__, __author_email__, __description__, __license__, __name__

CURRENT_PYTHON = sys.version_info[:2]
DORIAN_REQUIRED_PYTHON = (3, 6)

LOG_ZERO_MIN_VERSION = '1.5'
KAFKA_PYTHON_MIN_VERSION = '1.4'
BS4_MIN_VERSION = '4.7'

# This check and everything above must remain compatible with python 2.X.
##########################################################################
#                               INFO                                     #
#                         Unsupported Python                             #
##########################################################################

if CURRENT_PYTHON < DORIAN_REQUIRED_PYTHON:
    sys.stderr.write("""
    This version of Module requires Python {} {}, but you're trying to
    install it on Python {} {}
    """).format(*(DORIAN_REQUIRED_PYTHON + CURRENT_PYTHON))
    sys.exit(1)

REQUIREMENTS = [
    'logzero>={0}'.format(LOG_ZERO_MIN_VERSION),
    'kafka-python>={0}'.format(KAFKA_PYTHON_MIN_VERSION),
    'beautifulsoup4>={0}'.format(BS4_MIN_VERSION),
]

setup(
    name=__name__,
    # namespace_packages=['scale'],
    version=__version__,
    python_require='>{}.{}'.format(*DORIAN_REQUIRED_PYTHON),
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    package=find_packages(),
    license=__license__,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: 3'
        'Programming Language :: 3.5',
        'Programming Language :: 3.6',
        'Programming Language :: 3 :: only'
    ]
)
