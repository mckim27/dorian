#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import stat
import tarfile
from logzero import logger as log


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
            log.error('{0} attempt of {1}; error opening file: {2}'.format(attempts + 1, timeout, oe))
            os.umask(umask_original)
            time.sleep(sleep_int)
            return open_pipe(path_to_file, attempts + 1)
        finally:
            os.umask(umask_original)
    return None


def get_tar_stream(f_pipe):

    if f_pipe is None:
        log.error('error opening file: f_pipe is None')
        exit(-2)

    log.debug("Creating tarstream...")
    try:
        tar_stream = tarfile.open(fileobj=f_pipe, mode="w|", encoding='utf-8')
    except tarfile.TarError as te:
        log.error('error creating tarstream: {0}'.format(te))
        exit(-2)

    return tar_stream