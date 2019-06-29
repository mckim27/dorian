#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import fire
from logzero import logger as log
import sys
import argparse
from common.info_util import print_app_info
from common.factory import ActionFactory
from form.data import PipelineContentsData
from common import g_resource

g_resource.RUN_MODE = 'pipeline'

if __name__ == "__main__" :


    zero_arg = None
    base_argv = []
    fire_argv = []

    is_sep = False

    if not 'run' in sys.argv:
        log.error('The "run" param is required ... ')
        exit(135)

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

    sys.argv.clear()
    sys.argv.append(zero_arg)
    sys.argv = sys.argv + base_argv

    parser = argparse.ArgumentParser(description='plz put "--in_path, --out_path"')
    parser.add_argument('--in_path', type=str, nargs='?',
                        default=None,
                        help='resource input path')

    parser.add_argument('--out_path', type=str, nargs='?',
                        default=None,
                        help='result output path')

    parser.add_argument('--print_banner', type=int, nargs='?',
                        default=1,
                        help='is print banner param.  input int 1 or 0')

    args = parser.parse_args()

    if args.print_banner:
        print_app_info()

    log.info('base_argv : {0}'.format(', '.join(base_argv)))
    log.info('fire_argv : {0}'.format(', '.join(fire_argv)))

    in_path = args.in_path
    assert isinstance(in_path, str), 'the "in_path" param is invalid ... in_path : {}'.format(in_path)

    out_path = args.out_path
    assert isinstance(out_path, str), 'the "out_path" param is invalid ... out_path : {}'.format(out_path)

    g_resource.IN_PATH = in_path
    g_resource.OUT_PATH = out_path

    sys.argv.clear()
    sys.argv.append(zero_arg)
    sys.argv = sys.argv + fire_argv

    actionFactory = ActionFactory()

    for dirpath, dirs, files in os.walk(in_path):
        for file in files:
            with open(os.path.join(dirpath, file), encoding='utf-8') as f:
                # file_name = f.name[f.name.rfind('/') + 1 : -5]
                # log.debug(file_name)
                data = PipelineContentsData(f.name, f.read())

            actionFactory.set_data(data=data)

            fire.Fire(actionFactory)

            if len(fire_argv) == 0 or len(fire_argv) == 1:
                log.error('The "fire_argv" param must be greater than 1 ... ')
                exit(135)
