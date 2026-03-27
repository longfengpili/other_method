# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FLAC audio file management tool for batch processing audio files. It handles:
- Audio format conversion (WAV, MP3, M4A, OGG, AAC → FLAC)
- FLAC metadata editing (artist, title, album tags)
- Cover image management (add, clear, backup pictures)
- Batch processing of directories

## Architecture

### Core Modules
- `flac/__init__.py`: Audio format conversion (`convert_to_flac()`)
- `flac/flac_base.py`: Base class `FlacBase` for FLAC file operations
- `flac/flac_info.py`: Metadata management (`FlacInfo` class, updates tags via regex)
- `flac/flac_cover.py`: Cover image handling (`FlacCover` class, supports multiple picture types)

### Key Design Patterns
- **Inheritance**: `FlacInfo` and `FlacCover` inherit from `FlacBase`
- **Batch Processing**: `main.py` orchestrates the workflow: convert → update metadata → add covers
- **Configurable Processing**: Uses regex patterns to extract metadata from filenames
- **Picture Type Mapping**: `FlacCover._PICTURE_TYPE_MAP` defines FLAC picture type codes

### External Dependencies
- `mutagen`: Audio metadata manipulation (FLAC, ID3 tags)
- `pydub`: Audio format conversion
- `pydbapi.conf.LOGGING_CONFIG`: External logging configuration (shared module)

## Common Development Tasks

### Running the Tool
```bash
# Process a directory of audio files
python main.py
```

The `main.py` example shows typical usage:
- Processes files in `E:\music\QQ音乐 华语经典.九十年代盛行歌曲.甄选423首`
- Extracts artist/title using regex `(?P<artist>.+)-(?P<title>.+)`
- Sets album to "90年代盛行歌曲423首"
- Adds cover image from `e:/music/cover.jpg`

### Testing Changes
- No formal test suite exists; test with actual audio files
- Use small sample directories to verify conversion and metadata updates
- Check log output for errors (configured via `pydbapi.conf`)

### Adding New Features
1. **New audio format support**: Add to `supported_formats` in `flac/__init__.py`
2. **New metadata fields**: Extend `FlacInfo.update()` method
3. **New picture types**: Add to `FlacCover._PICTURE_TYPE_MAP`
4. **Processing pipeline**: Modify `modify_audios()` in `main.py`

## Code Patterns to Follow

### File Path Handling
- Use `Path` from `pathlib` for cross-platform compatibility
- Type alias `PathLike = Union[str, Path]` for flexible parameter types

### Error Handling
- Log errors with `logging.error()` but continue processing other files
- Return `None` or `False` on failure to allow batch continuation

### FLAC Operations
- Always call `self.delete()` before updating metadata (`FlacInfo.update()`)
- Save changes with `self.save('action_name')` for consistent logging
- FLAC compression level 8 (maximum) is used for smallest file size

## Important Notes

- **Logging**: Configured via external `pydbapi.conf.LOGGING_CONFIG` module
- **File Safety**: `remove_original=True` deletes source files after conversion (use cautiously)
- **Metadata Extraction**: Regex pattern must match filename format (e.g., "Artist - Title.flac")
- **Picture Types**: Supported types defined in `FlacCover._PICTURE_TYPE_MAP` (cover=3, back=4, etc.)

## Extension Points

1. **Additional audio formats**: Extend `convert_to_flac()` in `flac/__init__.py`
2. **Network sources**: Add URL download support for cover images
3. **Database integration**: Store metadata in SQL database alongside files
4. **Audio processing**: Integrate with audio effects or normalization libraries