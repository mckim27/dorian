#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
from form.base_proc import BaseProc
from common import config
from form.data import PipelineContentsData

class Scrapper(BaseProc):

    def __init__(self):
        super(Scrapper, self).__init__()

    def get_raw_html_from_spout(self):
        assert config.RUN_MODE == 'kafka_spout', \
            'this function is only `kafka_spout` run_mode...'

        for msg in config.CONSUMER_INSTANCE:
            data = PipelineContentsData(
                msg.key.decode('utf-8'), msg.value.decode('utf-8'))

            self._data_list.append(data)

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

        return self


    def scrap_daumnews_article_contents(self):

        for data in self._data_list:
            result_text = ''
            
            soup = BeautifulSoup(data.contents, 'html.parser')
            news_view = soup.find('div', class_='news_view')

            # log.debug(news_view)

            text_container = news_view.find('div', id='harmonyContainer')
            # text = text_container.find_all('section')
            re = text_container.find_all("p", attrs={"dmcf-ptype": True})

            for text_block in re:
                # log.debug(text_block.get_text())

                if result_text != '':
                    result_text = result_text.strip() + '\n'

                result_text += text_block.get_text().strip() + '\n'

            data.contents = result_text
            data.file_name = data.file_name + '.txt'

        return self