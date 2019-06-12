#! /usr/bin/python
# -*- coding: utf-8 -*-

import tarfile
import time
import os
import io
from common import config
from kafka import KafkaConsumer
from logzero import logger as log
from common.file_util import open_pipe, get_tar_stream

class BaseProc:

    _data_list = []

    def __init__(self):
        if config.RUN_MODE == 'kafka_spout' and config.CONSUMER_INSTANCE is None:
            log.debug('set kafka_consumer step')

            log.debug('topic_name : ' + config.TOPIC_NAME)
            log.debug('group_id : ' + config.GROUP_ID)
            log.debug('brokers : {0}'.format(','.join(config.BROKER_HOSTS)))

            config.CONSUMER_INSTANCE = KafkaConsumer(
                config.TOPIC_NAME,
                auto_offset_reset='latest', group_id=config.GROUP_ID,
                bootstrap_servers=config.BROKER_HOSTS, api_version=(0, 10),
                consumer_timeout_ms=5000, max_poll_records=10
            )

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