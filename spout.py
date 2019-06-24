#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import fire
import json
from logzero import logger as log
import sys
import argparse
import tarfile
import os
from common.info_util import print_app_info
from common.factory import ActionFactory
from kafka import KafkaConsumer
from form.data import PipelineContentsData
from common.file_util import get_tar_stream, open_pipe, add_dir_to_tarfile
from common import g_resource
from common.msg import ERR_INVALID_TYPE

g_resource.RUN_MODE = 'spout'
g_resource.SPOUT_DATA_COUNT_PER_ONCE = 30



if __name__ == "__main__" :
    print_app_info()

    log.debug('sys.argv : {0}'.format(', '.join(sys.argv)))

    zero_arg = None
    base_argv = []
    fire_argv = []

    is_sep = False

    for _,arg  in enumerate(sys.argv):
        if _ == 0 :
            zero_arg = arg
            continue

        if not is_sep and sys.argv[_] == 'run':
            is_sep = True
            continue

        if is_sep :
            fire_argv.append(arg)
        else :
            base_argv.append(arg)

    if not is_sep:
        log.error('"run" command is required ... ')
        exit(134)

    log.debug('base_argv : {0}'.format(', '.join(base_argv)))
    log.debug('fire_argv : {0}'.format(', '.join(fire_argv)))

    log.debug(zero_arg)

    sys.argv.clear()
    sys.argv.append(zero_arg)
    sys.argv = sys.argv + base_argv

    log.debug('base sys.argv : {0}'.format(', '.join(sys.argv)))

    parser = argparse.ArgumentParser(description='news crawler.')
    parser.add_argument('--broker_hosts', type=str, nargs='*',
                        default=['192.168.0.31:9092', '192.168.0.32:9092', '192.168.0.33:9092'],
                        help='kafka broker hosts')

    parser.add_argument('--topic_name', type=str, nargs='?',
                        default='news_raw_contents',
                        help='target topic name')

    parser.add_argument('--group_id', type=str, nargs='?',
                        default='daum_news_raw_contents_consumer',
                        help='consumer group id')

    parser.add_argument('--out_path', type=str, nargs='?',
                        default='/pfs/out',
                        help='result output folder path')

    args = parser.parse_args()
    broker_hosts = args.broker_hosts
    topic_name = args.topic_name
    group_id = args.group_id
    g_resource.OUT_PATH = args.out_path

    log.info('##### kafka config')
    log.info('# broker_hosts : {0}'.format(', '.join(broker_hosts)))
    log.info('# topic_name : {0}'.format(topic_name))
    log.info('# group_id : {0}'.format(group_id))
    log.info('# out_path : {0}'.format(g_resource.OUT_PATH))

    sys.argv.clear()
    sys.argv.append(zero_arg)
    sys.argv = sys.argv + fire_argv
    log.debug('fire sys.argv : {0}'.format(', '.join(sys.argv)))

    file_pipe = None
    tar_stream = None
    consumer = None

    actionFactory = ActionFactory()

    while True:
        log.info("wating ....")
        time.sleep(3)
        data_count = 0

        if consumer is None:
            consumer = KafkaConsumer(
                topic_name,
                auto_offset_reset='latest', group_id=group_id,
                bootstrap_servers=broker_hosts, api_version=(0, 10),
                consumer_timeout_ms=5000, max_poll_records=g_resource.SPOUT_DATA_COUNT_PER_ONCE,
                fetch_max_bytes=5000000
            )

        # TODO function 으로 만들수 있는 부분 생각해보고 function 변경하기.
        for msg in consumer:
            data_count += 1

            log.debug('data_count : {0}'.format(data_count))

            news_info = json.loads(msg.value)

            ymd_date = news_info['origin_create_date']
            ymd_date = ymd_date[:8]

            assert isinstance(news_info['category_en_name'], str), \
                ERR_INVALID_TYPE.format(news_info['category_en_name'])

            category_en_path = ymd_date + '/' + news_info['category_en_name']

            assert isinstance(news_info['sub_category_en_name'], str), \
                ERR_INVALID_TYPE.format(news_info['sub_category_en_name'])

            sub_category_en_name = news_info['sub_category_en_name']

            if sub_category_en_name != '-':
                category_en_path += '/' + sub_category_en_name

            if g_resource.SPOUT_FILE_PIPE is None:
                g_resource.SPOUT_FILE_PIPE = open_pipe(g_resource.OUT_PATH)
                g_resource.SPOUT_TAR_STREAM = get_tar_stream(g_resource.SPOUT_FILE_PIPE)
                log.debug('pipe and tar open !!!')
                add_dir_to_tarfile(category_en_path, g_resource.SPOUT_TAR_STREAM)

            data = PipelineContentsData(
                category_en_path + '/' + msg.key.decode('utf-8'), news_info['contents'])

            actionFactory.set_data(data=data)

            log.debug('Sleep to prevent the broken pipe.')
            time.sleep(2)

            fire.Fire(actionFactory)

            if data_count != 0 and data_count % g_resource.SPOUT_DATA_COUNT_PER_ONCE == 0:
                consumer.commit()

                g_resource.close_tar_stream_and_pipe()

                log.info('consumer commit. wait for next data.')
                time.sleep(2)

        if data_count != 0:
            g_resource.close_tar_stream_and_pipe()

        if len(fire_argv) == 0:
            log.error('"run" param is required ... ')
            exit(135)