#! /usr/bin/python
# -*- coding: utf-8 -*-

from scrap.scrapper import Scrapper
from cleanse.cleanser import Cleanser
from form.data import PipelineContentsData


class ActionFactory:

    def __init__(self):
        self.scrapper = None
        self.cleanser = None

    def set_data(self, data: PipelineContentsData = None):
        # set feature module
        self.scrapper = Scrapper(data)
        self.cleanser = Cleanser(data)
