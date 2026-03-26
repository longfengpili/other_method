from flac import convert_to_flac, FlacInfo, FlacCover

def modify_audios(filedir: str, name_regexp: str = None, pictures: dict = None, **kwargs):
    pictures = pictures or {}
    files = Path(filedir).glob('*')
    files = list(files)
    for file in files:
        if file.suffix in ['.wav', '.mp3', '.m4a', '.ogg', '.aac', '.flac']:
            file = convert_to_flac(file, remove_original=True)
        else:
            continue

        finfo = FlacInfo(file)
        finfo.update(name_regexp, **kwargs)
        fpic = FlacCover(file)
        fpic.add_pictures(pictures)



if __name__ == '__main__':
    pictures={'cover': 'e:/music/cover.jpg'}
    modify_audios(r'E:\music\QQ音乐 华语经典.九十年代盛行歌曲.甄选423首', name_regexp=r'(?P<artist>.+)-(?P<title>.+)', album='90年代盛行歌曲423首', pictures=pictures)
    