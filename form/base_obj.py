#! /usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tarfile
import time
import os
import io
from common import config
from kafka import KafkaConsumer
from logzero import logger as log
from common.file_util import open_pipe, get_tar_stream
from form.data import PipelineContentsData


class Module:

    _data = None

    def __init__(self, run_mode: str = 'pipeline', data: PipelineContentsData = None):
        self._RUN_MODE = run_mode
        self._data = data

    # def file_save(self):
    #     if self._RUN_MODE == 'pipeline':
    #         for data in self._data_list:
    #
    #             if data is None:
    #                 continue
    #
    #             file_path = os.path.join(config.OUT_PATH, data.file_name)
    #
    #             if os.path.exists(file_path):
    #                 log.wran('file exist... by pass. :: file_path - {0}'.format(file_path))
    #                 continue
    #
    #             with open(file_path, encoding='utf-8') as f:
    #                 f.write(data.contents)
    #
    #         log.debug('pipeline end and exit.')
    #         exit(0)
    #
    #     elif config.RUN_MODE == 'kafka_spout':
    #
    #         file_pipe = None
    #         tar_stream = None
    #         first_flag = True
    #
    #         for data in self._data_list:
    #             if data is None:
    #                 continue
    #
    #             if first_flag:
    #                 file_pipe = open_pipe(config.OUT_PATH)
    #                 tar_stream = get_tar_stream(file_pipe)
    #                 first_flag = False
    #
    #             tar_info = tarfile.TarInfo()
    #             tar_info.size = len(data.contents.encode('utf-8'))
    #             tar_info.mode = 0o600
    #             tar_info.name = data.file_name
    #             tar_info.mtime = time.time()
    #
    #             try:
    #                 with io.BytesIO(data.contents.encode('utf-8')) as ff:
    #                     tar_stream.addfile(tarinfo=tar_info, fileobj=ff)
    #
    #             except tarfile.TarError as te:
    #                 raise Exception('error writing contents {0} to tarstream: {1}'.format(data.contents, data.file_name))
    #
    #         if not first_flag:
    #             tar_stream.close()
    #             file_pipe.close()
    #             log.debug('data_file save complete.')
    #
    #     self._data_list.clear()
