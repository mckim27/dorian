#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from form.base_obj import Module
from common import config


class Cleanser(Module):

    def __init__(self, run_mode, data):
        super(Cleanser, self).__init__(run_mode, data)

    def cleanse_news_text(self):
        log.debug('cleanse_news_text')
        return self

    def end(self):
        if config.RUN_MODE == 'pipeline':
            log.debug('pipeline end and exit.')
            exit(0)
        elif config.RUN_MODE == 'kafka_spout':
            log.debug('kafka_spout end.')