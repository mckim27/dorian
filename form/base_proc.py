#! /usr/bin/python
# -*- coding: utf-8 -*-

from common import config
from kafka import KafkaConsumer
from logzero import logger as log


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