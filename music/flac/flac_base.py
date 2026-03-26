from pathlib import Path
from mutagen.flac import FLAC
from typing import Union, List, Tuple, Optional
import logging

from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

# 类型别名
PathLike = Union[str, Path]


class FlacBase:

    def __init__(self, flac_path: PathLike):
        self.file = Path(flac_path)
        self.audio = FLAC(flac_path) if self.file.exists() else None

    @property
    def exists(self) -> bool:
        """文件是否存在"""
        return self.file.exists()

    def delete(self):
        self.audio.delete()

    def save(self, action) -> bool:
        """保存更改"""
        try:
            self.audio.save()
            logging.info(f'{self.file.stem} modify {action} completed ~')
            return True
        except Exception:
            return False
