#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import io
import os
import sys
import stat
import tarfile
from kafka import KafkaConsumer
from scrap.daum_news_scrapper import ex_scrap

# SPOUT = '/pfs/out'
SPOUT = './pfs/out'


def open_pipe(path_to_file, attempts=0, timeout=2, sleep_int=5):
    if attempts < timeout :
        flags = os.O_WRONLY  # Refer to "man 2 open".
        mode = stat.S_IWUSR  # This is 0o400.
        umask = 0o777 ^ mode  # Prevents always downgrading umask to 0.
        umask_original = os.umask(umask)
        try:
            file = os.open(path_to_file, flags, mode)
            # you must open the pipe as binary to prevent line-buffering problems.
            return os.fdopen(file, "wb")
        except OSError as oe:
            print ('{0} attempt of {1}; error opening file: {2}'.format(attempts + 1, timeout, oe))
            os.umask(umask_original)
            time.sleep(sleep_int)
            return open_pipe(path_to_file, attempts + 1)
        finally:
            os.umask(umask_original)
    return None


def get_tar_stream(ex_spout):

    if ex_spout is None:
        print('error opening file: {}'.format(SPOUT))
        exit(-2)

    print("Creating tarstream...")
    try:
        tarStream = tarfile.open(fileobj=ex_spout, mode="w|", encoding='utf-8')
    except tarfile.TarError as te:
        print('error creating tarstream: {0}'.format(te))
        exit(-2)

    return tarStream


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

        first_flag = True

        news_meta_info_list = []

        tar_stream = None
        file_pipe = None

        for msg in consumer:
            if first_flag:
                file_pipe = open_pipe(SPOUT)
                tarStream = get_tar_stream(file_pipe)

            print(msg.key.decode('utf-8'))
            print(msg.value.decode('utf-8'))

            raw_html = msg.value.decode('utf-8')
            name = msg.key.decode('utf-8')

            contents = ex_scrap(raw_html).strip()

            textIO = io.TextIOWrapper(io.BytesIO(), encoding='utf8')
            textIO.write(contents)
            bytesIO = textIO.detach()
            info = tarfile.TarInfo(name=name)
            info.size = bytesIO.tell()

            try:
                tarStream.addfile(tarinfo=info, fileobj=bytesIO)

            except tarfile.TarError as te:
                print('error writing contents {0} to tarstream: {1}'.format(contents, name))
                exit(-2)

        if not first_flag:
            tar_stream.close()
            file_pipe.close()