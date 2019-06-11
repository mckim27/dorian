#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import io
import os
import stat
import tarfile
from kafka import KafkaConsumer
from scrap.daum_news_scrapper import ex_scrap
from logzero import logger as log
from common.file_util import get_tar_stream, open_pipe

SPOUT = '/pfs/out'
# SPOUT = './pfs/out'

if __name__ == "__main__" :
    brokers = ['192.168.0.31:9092', '192.168.0.32:9092', '192.168.0.33:9092']
    consumer = KafkaConsumer(
        'news_raw_contents',
        auto_offset_reset='latest', group_id='daum_news_raw_contents_consumer',
        bootstrap_servers=brokers, api_version=(0, 10),
        consumer_timeout_ms=5000, max_poll_records=10
    )

    while True:
        log.info("wating ....")
        time.sleep(3)

        first_flag = True

        news_meta_info_list = []

        tar_stream = None
        file_pipe = None

        for msg in consumer:
            if first_flag:
                file_pipe = open_pipe(SPOUT)
                tar_stream = get_tar_stream(file_pipe)
                first_flag = False

            # print(msg.key.decode('utf-8'))
            # print(msg.value.decode('utf-8'))

            raw_html = msg.value.decode('utf-8')
            name = msg.key.decode('utf-8')

            contents = ex_scrap(raw_html)
            log.debug("contents : " + contents)

            tarHeader = tarfile.TarInfo()
            tarHeader.size = len(contents.encode('utf-8'))
            tarHeader.mode = 0o600
            tarHeader.name = name
            tarHeader.mtime = time.time()

            try:
                with io.BytesIO(contents.encode('utf-8')) as ff:
                    tar_stream.addfile(tarinfo=tarHeader, fileobj=ff)

            except tarfile.TarError as te:
                log.error('error writing contents {0} to tarstream: {1}'.format(contents, name))
                exit(-2)

        if not first_flag:
            tar_stream.close()
            file_pipe.close()
            log.debug('close~~~~')
