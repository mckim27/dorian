#! /usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tarfile
import time
import os
import io
from pathlib import Path
from logzero import logger as log
from form.data import PipelineContentsData
from common import g_resource


class Module:

    _data = None
    _status = 0
    _retry = 0

    def __init__(self, data: PipelineContentsData = None):
        self._data = data

    def clear_data(self):
        self._data = None
        self._status = None
        self._retry = None

    def set_data(self, data: PipelineContentsData = None):
        self._data = data

    def file_save(self):
        if self._status < 0:
            log.error('status is abnormal ... status : {0}'.format(self._status))
            return

        if g_resource.RUN_MODE == 'pipeline':

            if self._data is None:
                return

            self._data.file_name = \
                self._data.file_name.replace(g_resource.IN_PATH, g_resource.OUT_PATH)
            file_path = self._data.file_name.replace('html', 'txt')
            dir_path = file_path[:file_path.rfind('/')]

            log.debug('g_resource.OUT_PATH : {}'.format(g_resource.OUT_PATH))
            log.debug('target file_path : {}'.format(file_path))
            log.debug('target folder_path: {}'.format(dir_path))

            Path(dir_path).mkdir(parents=True, exist_ok=True)

            if os.path.exists(file_path):
                log.wran('file exist... by pass. :: file_path - {0}'.format(file_path))
                return

            with open(file_path, 'w', encoding='utf-8') as f:
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
                log.info('check tarstrem : {0}'.format(g_resource.SPOUT_TAR_STREAM))
                
                with io.BytesIO(self._data.contents.encode('utf-8')) as ff:
                    g_resource.SPOUT_TAR_STREAM.addfile(tarinfo=tar_info, fileobj=ff)

                self._retry = 0

            except Exception as e:
                if 'Broken pipe' in e.message:
                    log.warn('Broken pipe !!! wait a moment...')
                    time.sleep(5)

                    if self._retry != 3:
                        log.warn('retry count : {0}'.format(self._retry))
                        self._retry += 1
                        self.file_save()
                    else:
                        raise Exception(
                            'broken pipe error writing contents {0} to tarstream: {1}'.format(
                                self._data.contents, self._data.file_name))
                else:

                    raise Exception(
                        'error writing contents {0} to tarstream: {1}'.format(
                            self._data.contents, self._data.file_name))
