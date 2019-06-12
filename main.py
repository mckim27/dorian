#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import fire
from logzero import logger as log
from scrap.scrapper import Scrapper
from cleanse.cleanser import Cleanser
from common import config


class ActionFactory:

    def __init__(self, run_mode='pipeline', in_path=None, out_path='/pfs/out',
                 broker_hosts=None, topic_name=None, group_id=None, ):
        # set contant value
        config.RUN_MODE = run_mode
        config.IN_PATH = in_path
        config.OUT_PATH = out_path

        if broker_hosts is None:
            config.BROKER_HOSTS = ['192.168.0.31:9092', '192.168.0.32:9092', '192.168.0.33:9092']

        if topic_name is None:
            config.TOPIC_NAME = 'news_raw_contents'

        if group_id is None:
            config.GROUP_ID = 'daum_news_raw_contents_consumer'

        self.scrapper = Scrapper()
        self.cleanser = Cleanser()


if __name__ == "__main__" :
    while True:
        log.info("wating ....")
        time.sleep(3)
        fire.Fire(ActionFactory)