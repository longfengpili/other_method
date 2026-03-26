import re
from pathlib import Path
from mutagen.flac import FLAC
from typing import Union, List, Tuple, Optional
import logging

from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)


from .flac_base import FlacBase

# 类型别名
PathLike = Union[str, Path]


class FlacInfo(FlacBase):

    def __init__(self, flac_path: PathLike):
        super(FlacInfo, self).__init__(flac_path)

    def update(self, name_regexp: str = None, **kwargs):
        update_info = {}
        name = self.file.stem
        logging.info(f'{name} modify info starting ~')
        self.delete()

        if name_regexp:
            result = re.match(name_regexp, name)
            if not result:
                raise ValueError(f'{name} not match name_regexp: {name_regexp}')
            update_info.update(result.groupdict())

        if kwargs:
            update_info.update(kwargs)

        for k, v in update_info.items():
            self.audio[k.strip()] = v.strip()

        return self.save('FlacInfo')

