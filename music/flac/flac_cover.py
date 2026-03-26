from pathlib import Path
from mutagen.flac import FLAC, Picture
from typing import Union, List, Dict, Optional

from .flac_base import FlacBase

# 类型别名
PathLike = Union[str, Path]

import logging

from pydbapi.conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)


class FlacCover(FlacBase):
    """FLAC 封面管理器"""
     # 类级别的类型映射，避免每次调用都创建
    _PICTURE_TYPE_MAP = {
        'cover': 3,      # 专辑封面
        'front': 3,      # 封面（同义词）
        'back': 4,       # 封底
        'leaflet': 5,    # 宣传页
        'cd': 6,         # CD盘面
        'artist': 7,     # 主唱/艺人
        'band': 8,       # 乐队合照
        'composer': 11,  # 作曲家
        'logo': 19,      # 乐队标志
    }
    
    
    def __init__(self, flac_path: PathLike):
        super(FlacCover, self).__init__(flac_path)
    
    @property
    def has_pictures(self) -> bool:
        """是否有图片"""
        return bool(self.audio.pictures) if self.audio else False
    
    def get_picture_info(self) -> List[dict]:
        """获取所有图片信息"""
        if not self.audio:
            return []
        
        infos = []
        for i, pic in enumerate(self.audio.pictures):
            infos.append({
                "index": i,
                "type": pic.type,
                "mime": pic.mime,
                "desc": getattr(pic, "desc", ""),
                "size": len(pic.data)
            })
        return infos
    
    def clear_all_pictures(self) -> bool:
        """清除所有图片"""
        if not self.audio:
            return False
        
        self.audio.clear_pictures()
        return self.save('ClearPics')
    
    def add_picture(self, img_path: PathLike, pic_type: str = 'cover', desc: str = "") -> bool:
        """
        从文件添加图片 
        """

        logging.info(f'{self.file.stem} add pic {pic_type} starting ~')

        if not self.audio:
            return False

        # 获取类型值
        type_value = self._PICTURE_TYPE_MAP.get(pic_type.lower())
        if type_value is None:
            logging.error(f'{self.file.stem}: not support "{pic_type}"')
            return False
        
        img_path = Path(img_path)
        if not img_path.exists():
            logging.error(f'{self.file.stem}: pic not exists ! {img_path}')
            return False
        
        try:
            image_data = img_path.read_bytes()
            pic = Picture()
            pic.data = image_data
            
            # 设置 MIME
            suffix = img_path.suffix.lower()
            if suffix in ['.jpg', '.jpeg']:
                pic.mime = "image/jpeg"
            elif suffix == '.png':
                pic.mime = "image/png"
            else:
                return False
            
            pic.type = type_value
            pic.desc = desc or self._get_type_name(type_value)
            self.audio.add_picture(pic)

            if self.save(f'AddPic[{pic_type}]'):
                logging.info(f'{self.file.stem} add {pic_type} end ~')
            else:
                logging.error(f'{self.file.stem} add {pic_type} fail ~')
            
        except Exception:
            return False

    def add_pictures(self, pictures: Dict[str, PathLike], clear_all: bool = True):
        if not self.audio:
            return {k: False for k in pictures.keys()}
        
        if clear_all:
            self.clear_all_pictures()

        for pic_type, img_path in pictures.items():
            self.add_picture(img_path=img_path, pic_type=pic_type, desc=pic_type)

    def backup_pictures(self, output_dir: PathLike) -> List[Path]:
        """备份所有图片到指定目录"""
        if not self.audio or not self.audio.pictures:
            return []
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        for i, pic in enumerate(self.audio.pictures):
            # 确定扩展名
            ext = "jpg" if "jpeg" in pic.mime else "png"
            filename = f"{self.flac_path.stem}_pic{i}_type{pic.type}.{ext}"
            output_path = output_dir / filename
            
            output_path.write_bytes(pic.data)
            saved_files.append(output_path)
        
        return saved_files
