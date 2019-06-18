#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
from form.base_obj import Module
from common import config
from form.data import PipelineContentsData
from logzero import logger as log


class Scrapper(Module):

    def __init__(self, run_mode, data):
        super(Scrapper, self).__init__(run_mode, data)

    def get_raw_html_from_spout(self):
        assert config.RUN_MODE == 'kafka_spout', \
            'this function is only `kafka_spout` run_mode...'

        for msg in config.CONSUMER_INSTANCE:
            data = PipelineContentsData(
                msg.key.decode('utf-8'), msg.value.decode('utf-8'))

            self._data_list.append(data)

        log.info('get_raw_html_from_spout func end.')

        return self

    def get_raw_html_from_repo(self):
        assert config.RUN_MODE == 'pipeline', \
            'this function is only `pipeline` run_mode...'

        assert config.IN_PATH is not None, \
            'this function must need `constant.IN_PATH`...'

        for dirpath, dirs, files in os.walk(config.IN_PATH):
            for file in files:
                with open(os.path.join(dirpath, file), encoding='utf-8') as f:
                    data = PipelineContentsData(f.name, f.read())

                self._data_list.append(data)

        log.info('get_raw_html_from_repo func end.')

        return self


    def scrap_daumnews_article_contents(self):
        for idx, data in enumerate(self._data_list):
            result_text = ''

            soup = BeautifulSoup(data.contents, 'html.parser')
            news_view = soup.find('div', class_='news_view')

            if news_view is None:
                log.warn('not html .... ???')
                log.warn(news_view)
                self._data_list[idx] = None
                continue

            text_container = news_view.find('div', id='harmonyContainer')
            # text = text_container.find_all('section')
            re = text_container.find_all("p", attrs={"dmcf-ptype": True})

            for text_block in re:
                # log.debug(text_block.get_text())

                if result_text != '':
                    result_text = result_text.strip() + '\n'

                result_text += text_block.get_text().strip() + '\n'

            log.debug("result scrap file_name : " + data.file_name + '.txt')
            log.debug("result scrap text : " + result_text)

            data.contents = result_text
            data.file_name = data.file_name + '.txt'

        log.info('scrap_daumnews_article_contents func end.')

        return self