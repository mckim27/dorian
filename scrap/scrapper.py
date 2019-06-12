#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import io
import time
import tarfile
from logzero import logger as log
from bs4 import BeautifulSoup
from form.base_proc import BaseProc
from common import config
from common.file_util import open_pipe, get_tar_stream
from form.data import PipelineContentsData

class Scrapper(BaseProc):

    def __init__(self):
        super(Scrapper, self).__init__()

    def get_raw_html_from_spout(self):
        assert config.RUN_MODE == 'kafka_spout', \
            'this function is only `kafka_spout` run_mode...'

        for msg in config.CONSUMER_INSTANCE:
            data = PipelineContentsData()

            raw_html = msg.value.decode('utf-8')
            name = msg.key.decode('utf-8')

            data.contents = raw_html
            data.file_name = name

            self._data_list.append(data)

        return self

    def get_raw_html_from_repo(self):
        assert config.RUN_MODE == 'pipeline', \
            'this function is only `pipeline` run_mode...'

        assert config.IN_PATH is not None, \
            'this function must need `constant.IN_PATH`...'

        for dirpath, dirs, files in os.walk(config.IN_PATH):
            for file in files:
                data = PipelineContentsData()

                with open(os.path.join(dirpath, file), encoding='utf-8') as f:
                    data.contents = f.read()
                    data.file_name = f.name

                self._data_list.append(data)

        return self


    def scrap_daumnews_article_contents(self):

        for data in self._data_list:

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


    def file_save(self):
        if config.RUN_MODE == 'pipeline':
            for data in self._data_list:
                with open(
                        os.path.join(config.OUT_PATH, data.file_name),
                        encoding='utf-8') as f:
                    f.write(data.contents)

            log.debug('pipeline end and exit.')
            exit(0)

        elif config.RUN_MODE == 'kafka_spout':

            file_pipe = None
            tar_stream = None
            first_flag = True

            for data in self._data_list:
                if first_flag:
                    file_pipe = open_pipe(config.OUT_PATH)
                    tar_stream = get_tar_stream(file_pipe)
                    first_flag = False

                tar_info = tarfile.TarInfo()
                tar_info.size = len(data.contents.encode('utf-8'))
                tar_info.mode = 0o600
                tar_info.name = data.file_name
                tar_info.mtime = time.time()

                try:
                    with io.BytesIO(data.contents.encode('utf-8')) as ff:
                        tar_stream.addfile(tarinfo=tar_info, fileobj=ff)

                except tarfile.TarError as te:
                    raise Exception('error writing contents {0} to tarstream: {1}'.format(data.contents, data.file_name))

            if not first_flag:
                tar_stream.close()
                file_pipe.close()

            log.debug('data_file save.')
