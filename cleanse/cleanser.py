#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from form.base_proc import BaseProc
from common import config


class Cleanser(BaseProc):

    def __init__(self):
        super(Cleanser, self).__init__()

    def cleanse_news_text(self):
        log.debug('cleanse_news_text')
        return self

    def end(self):
        if constant.RUN_MODE == 'pipeline':
            log.debug('pipeline end and exit.')
            exit(0)
        elif constant.RUN_MODE == 'kafka_spout':
            log.debug('kafka_spout end.')