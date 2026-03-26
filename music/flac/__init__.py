from .flac_base import FlacBase
from .flac_info import FlacInfo
from .flac_cover import FlacCover



from pathlib import Path
from mutagen.id3 import ID3, TALB, COMM, TPE1, Encoding
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from pydub import AudioSegment
from typing import Union, List, Tuple, Optional
import logging

from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

# 类型别名
PathLike = Union[str, Path]

def convert_to_flac(input_path: PathLike, output_path: PathLike = None, remove_original: bool = False) -> str:
    """
    将音频文件转换为 FLAC 格式
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选，默认为输入文件同目录同名的.flac文件）
        remove_original: 是否删除原文件
    Returns:
        转换后的 FLAC 文件路径
    """
    file = Path(input_path)
    try:
        # 检查输入文件是否存在
        if not file.exists():
            logging.error(f"输入文件不存在: {input_path}")
            return None

        # 检查文件格式
        fsuffix = file.suffix
        supported_formats = ['.wav', '.mp3', '.m4a', '.ogg', '.aac', '.flac']

        if fsuffix not in supported_formats:
            logging.error(f"不支持的文件格式: {fsuffix}，支持格式: {supported_formats}")
            return None

        # 自动生成输出路径
        output_path = output_path or file.with_suffix('.flac').as_posix()

        logging.info(f"开始转换flac: {input_path}")

        # 加载音频文件
        if fsuffix == '.wav':
            audio = AudioSegment.from_wav(input_path)
        elif fsuffix == '.mp3':
            audio = AudioSegment.from_mp3(input_path)
        elif fsuffix == '.m4a':
            audio = AudioSegment.from_file(input_path, format='m4a')
        elif fsuffix == '.ogg':
            audio = AudioSegment.from_ogg(input_path)
        elif fsuffix == '.flac':
            audio = AudioSegment.from_file(input_path, format='flac')
        else:
            # 使用通用加载方法
            audio = AudioSegment.from_file(input_path)

        # 导出为 FLAC
        audio.export(
            output_path,
            format="flac",
            parameters=["-compression_level", "8"],  # FLAC 压缩级别 0-8，LAC 的压缩级别只影响编码效率，不影响音质, 8文件最小
            id3v2_version="3",  # 兼容 Windows
        )

        logging.debug(f"转换成功flac: {output_path}")

        # 可选：删除原文件
        if remove_original and fsuffix != '.flac':
            file.unlink()
            logging.warning(f"删除原文件: {input_path}")

        return output_path
    except Exception as e:
        logging.error(f"转换失败: {input_path} -> 错误: {e}")
        return None
