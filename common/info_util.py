#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
import coverage


def print_app_info():
    log.info('banner !!!!')
    log.info('{0}'.format(coverage.__name__))
    log.info('license : {0}'.format(coverage.__license__))
    log.info('version : {0}'.format(coverage.__version__))
    log.info('author : {0}'.format(coverage.__author__))
    log.info('contact : {0}'.format(coverage.__author_email__))
