# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2024-08-23 10:51:34
# @Last Modified by:   longfengpili
# @Last Modified time: 2024-09-01 11:08:45
# @github: https://github.com/longfengpili

from pathlib import Path

from pydbapi.conf import LOGGING_CONFIG
import ffmpeg

import logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def get_files(path: str = None):
    path = path or './'
    path = Path(path)
    files = [file for file in path.rglob('*.mp4')]
    return files


def convert_video(file: Path, target_path: str = None, r: int = 60):
    file = file.resolve()
    target_path = target_path or f'{file.drive}/'
    tpath = Path(target_path) / 'new_video'
    tfile = tpath / f'new_{file.name}'
    tfile = tfile.as_posix()

    if not tpath.exists():
        tpath.mkdir(parents=True)

    ffmpeg.input(file).output(tfile, r=r).run()


if __name__ == '__main__':
    files = get_files()
    for file in files:
        logger.info(file)
        convert_video(file)
        break
