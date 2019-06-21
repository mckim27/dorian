#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from common.info_util import print_app_info

if __name__ == "__main__" :
    print_app_info()