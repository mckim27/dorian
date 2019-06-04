#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
from kafka import KafkaConsumer

if __name__ == "__main__" :
    brokers = ['192.168.0.31:9092', '192.168.0.32:9092', '192.168.0.33:9092']
    consumer = KafkaConsumer(
        'news_raw_contents',
        auto_offset_reset='latest', group_id='daum_news_raw_contents_consumer',
        bootstrap_servers=brokers, api_version=(0, 10),
        consumer_timeout_ms=5000, max_poll_records=10
    )

    while True:
        print("wating ....")
        time.sleep(3)

        news_meta_info_list = []

        for msg in consumer:
            print(msg.key.decode('utf-8'))
            print(msg.value.decode('utf-8'))