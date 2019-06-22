#! /usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tarfile
import time
import os
import io
from logzero import logger as log
from form.data import PipelineContentsData
from common import g_resource


class Module:

    _data = None
    _status = 0

    def __init__(self, data: PipelineContentsData = None):
        self._data = data


    def set_data(self, data: PipelineContentsData = None):
        self._data = data

    def file_save(self):
        if self._status < 0:
            log.error('status is abnormal ... status : {0}'.format(self._status))
            return

        if g_resource.RUN_MODE == 'pipeline':

            if self._data is None:
                return

            file_path = os.path.join(g_resource.OUT_PATH, self._data.file_name)

            if os.path.exists(file_path):
                log.wran('file exist... by pass. :: file_path - {0}'.format(file_path))
                return

            with open(file_path, encoding='utf-8') as f:
                f.write(self._data.contents)

            log.debug('pipeline file save and exit.')
        else:
            if self._data is None:
                return

            tar_info = tarfile.TarInfo()
            tar_info.size = len(self._data.contents.encode('utf-8'))
            tar_info.mode = 0o600
            tar_info.name = self._data.file_name
            tar_info.mtime = time.time()

            try:
                with io.BytesIO(self._data.contents.encode('utf-8')) as ff:
                    g_resource.SPOUT_TAR_STREAM.addfile(tarinfo=tar_info, fileobj=ff)

            except tarfile.TarError as te:
                raise Exception('error writing contents {0} to tarstream: {1}'.format(self._data.contents, self._data.file_name))
