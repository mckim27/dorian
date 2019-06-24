#! /usr/bin/python
# -*- coding: utf-8 -*-

RUN_MODE = None
IN_PATH = None
OUT_PATH = None

SPOUT_FILE_PIPE = None
SPOUT_TAR_STREAM = None

SPOUT_DATA_COUNT_PER_ONCE = 30

def close_tar_stream_and_pipe():
    if SPOUT_TAR_STREAM is not None:
        SPOUT_TAR_STREAM.close()

    if SPOUT_TAR_STREAM is not None:
        SPOUT_TAR_STREAM.close()