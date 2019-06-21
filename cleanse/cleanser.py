#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from form.base_obj import Module
from common import config


class Cleanser(Module):

    def __init__(self, data):
        super(Cleanser, self).__init__(data)

    def cleanse_news_text(self):
        log.debug('cleanse_news_text')
        return self
