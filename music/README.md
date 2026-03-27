# FLAC 音频文件管理器

一个用于批量处理音频文件的Python工具：格式转换、元数据编辑和封面图片管理。

## 功能特性

- **格式转换**：将 WAV、MP3、M4A、OGG、AAC 转换为 FLAC 格式，支持可配置的压缩级别
- **元数据提取**：使用正则表达式从文件名中提取艺术家、标题等元数据
- **封面管理**：添加、清除和备份 FLAC 文件的封面图片
- **批量处理**：一次性处理整个目录的音频文件
- **无损音质**：FLAC 转换保持音频质量的同时减小文件大小

## 安装

### 环境要求
- Python 3.7+
- FFmpeg（pydub 音频转换所需）

### 安装依赖
```bash
pip install mutagen pydub
```

`pydbapi` 模块似乎是项目特定的日志配置模块。

## 使用方法

### 基本命令
```bash
python main.py
```

### 自定义处理
修改 `main.py` 以适应您的需求：
```python
from flac import convert_to_flac, FlacInfo, FlacCover
from pathlib import Path

def process_audio_directory(directory, name_pattern, album_name, cover_image):
    pictures = {'cover': cover_image}
    files = Path(directory).glob('*')

    for file in files:
        if file.suffix in ['.wav', '.mp3', '.m4a', '.ogg', '.aac', '.flac']:
            # 转换为 FLAC（如果需要）
            flac_file = convert_to_flac(file, remove_original=True)

            # 更新元数据
            finfo = FlacInfo(flac_file)
            finfo.update(name_pattern, album=album_name)

            # 添加封面图片
            fpic = FlacCover(flac_file)
            fpic.add_pictures(pictures)
```

## 示例

### 示例 1：基础处理
```python
# 处理目录中的音频文件
pictures = {'cover': 'e:/music/cover.jpg'}
modify_audios(
    r'E:\music\QQ音乐 华语经典.九十年代盛行歌曲.甄选423首',
    name_regexp=r'(?P<artist>.+)-(?P<title>.+)',
    album='90年代盛行歌曲423首',
    pictures=pictures
)
```

### 示例 2：自定义元数据提取
```python
# 提取音轨号和标题："01 - Song Title.flac"
finfo.update(r'(?P<track>\d+)\s*-\s*(?P<title>.+)')

# 提取艺术家、专辑、标题："Artist - Album - Title.flac"
finfo.update(r'(?P<artist>.+)\s*-\s*(?P<album>.+)\s*-\s*(?P<title>.+)')
```

### 示例 3：多个封面图片
```python
pictures = {
    'cover': 'front.jpg',      # 专辑封面（类型 3）
    'back': 'back.jpg',        # 封底（类型 4）
    'artist': 'singer.jpg',    # 艺人照片（类型 7）
    'logo': 'band_logo.png'    # 乐队标志（类型 19）
}
fpic.add_pictures(pictures, clear_all=True)
```

## 项目结构

```
music/
├── main.py              # 批量处理入口点
├── README.md           # 本文档
├── CLAUDE.md          # Claude Code 指导文件
└── flac/              # 核心 FLAC 处理模块
    ├── __init__.py    # 音频格式转换
    ├── flac_base.py   # 基础 FLAC 操作
    ├── flac_info.py   # 元数据管理
    └── flac_cover.py  # 封面图片处理
```

### 模块详情

- **`flac/__init__.py`**：`convert_to_flac()` 函数，用于格式转换
- **`flac/flac_base.py`**：`FlacBase` 类，包含文件操作和保存功能
- **`flac/flac_info.py`**：`FlacInfo` 类，用于元数据提取和更新
- **`flac/flac_cover.py`**：`FlacCover` 类，用于管理 FLAC 图片

## API 参考

### `convert_to_flac(input_path, output_path=None, remove_original=False)`
将音频文件转换为 FLAC 格式。

**参数：**
- `input_path`：源音频文件路径
- `output_path`：可选输出路径（默认：相同名称，扩展名为 .flac）
- `remove_original`：转换后删除源文件（默认：False）

**返回：** 转换后的 FLAC 文件路径，失败时返回 `None`

### `FlacInfo(flac_path)`
管理 FLAC 元数据。

**方法：**
- `update(name_regexp=None, **kwargs)`：从正则表达式或关键字参数更新元数据
- `delete()`：清除现有元数据
- `save(action)`：保存更改到文件

### `FlacCover(flac_path)`
管理 FLAC 封面图片。

**属性：**
- `has_pictures`：检查文件是否包含嵌入图片

**方法：**
- `add_picture(img_path, pic_type='cover', desc="")`：添加单个图片
- `add_pictures(pictures, clear_all=True)`：添加多个图片
- `clear_all_pictures()`：移除所有嵌入图片
- `get_picture_info()`：列出所有嵌入图片信息
- `backup_pictures(output_dir)`：提取图片到文件

**支持的图片类型：** `cover`, `front`, `back`, `leaflet`, `cd`, `artist`, `band`, `composer`, `logo`

## 配置

### 日志记录
项目使用来自 `pydbapi.conf.LOGGING_CONFIG` 的共享日志配置。
可以修改此模块或实现自己的日志配置。

### FLAC 压缩
在 `convert_to_flac()` 中压缩级别设置为 8（最大值）以获得最小文件大小。
FLAC 压缩只影响编码效率，不影响音频质量。

## 常见模式

### 文件名格式化
工具期望一致的文件名模式用于元数据提取：
- `Artist - Title.flac`
- `Track - Title.flac`
- `Artist - Album - Title.flac`

### 批量处理流程
`main.py` 中的 `modify_audios()` 函数展示了完整工作流程：
1. 将音频文件转换为 FLAC
2. 从文件名提取元数据
3. 更新 FLAC 标签
4. 添加封面图片

## 故障排除

### "输入文件不存在"
- 检查文件路径和权限
- 确保文件扩展名在支持格式中

### "文件格式不支持"
- 支持格式：`.wav`, `.mp3`, `.m4a`, `.ogg`, `.aac`, `.flac`
- 安装 FFmpeg 以使 `pydub` 能处理所有格式

### "名称不匹配正则表达式"
- 验证正则表达式模式是否匹配文件名格式
- 使用像 `(?P<artist>.+)` 这样的命名组进行提取

### "图片类型不支持"
- 使用其中之一：`cover`, `front`, `back`, `leaflet`, `cd`, `artist`, `band`, `composer`, `logo`
- 检查文件是否存在且为 JPEG/PNG 格式

## 扩展工具

### 添加新音频格式
1. 在 `flac/__init__.py` 的 `supported_formats` 中添加格式
2. 在 `convert_to_flac()` 中添加加载逻辑

### 添加新元数据字段
1. 扩展 `FlacInfo.update()` 以处理新字段
2. 更新正则表达式模式以提取新字段

### 添加新图片类型
1. 添加到 `FlacCover._PICTURE_TYPE_MAP` 字典
2. 使用标准 FLAC 图片类型代码

## 许可证

本项目可供使用和修改。有关特定许可信息，请参阅各个文件。