#! /usr/bin/python
# -*- coding: utf-8 -*-

from logzero import logger as log
from scrap.scrapper import Scrapper
from cleanse.cleanser import Cleanser
from form.data import PipelineContentsData


class ActionFactory:

    def __init__(self):
        self.scrapper = None
        self.cleanser = None

    def set_data(self, data: PipelineContentsData = None):
        # set feature module
        if self.scrapper is None:
            self.scrapper = Scrapper(data)
            self.cleanser = Cleanser(data)
        else:
            self.scrapper.set_data(data)
            self.cleanser.set_data(data)