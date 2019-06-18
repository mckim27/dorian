#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import fire
from logzero import logger as log
from scrap.scrapper import Scrapper
from cleanse.cleanser import Cleanser
from form.data import PipelineContentsData


class ActionFactory:

    def __init__(self, run_mode: str = 'pipeline', data: PipelineContentsData = None):

        # set feature module
        self.scrapper = Scrapper(run_mode, data)
        self.cleanser = Cleanser(run_mode, data)




