# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2022-01-20 12:19:43
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-01-20 13:30:43


import os
import json
import time
import requests
import shutil
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

import m3u8
from Crypto.Cipher import AES

import logging
import colorlog
log_colors_config = {
    'DEBUG': 'cyan',
    # 'INFO': 'yellow',
    'WARNING': 'red',
    'ERROR': 'red',
    'CRITICAL': 'red',
}
formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(log_color)s%(message)s',
            log_colors=log_colors_config)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
dm3u8 = logging.getLogger(__name__)
dm3u8.addHandler(handler)
dm3u8.setLevel(logging.DEBUG)


class DownloadM3U8:

    def __init__(self, m3u8_url):
        self.m3u8_url = m3u8_url

    def myrequests_get(self, url, headers=None, verify=False):
        try:
            res = requests.get(url, headers=headers, verify=verify, timeout=60) 
        except Exception as e:
            dm3u8.error(f"request 【{url}】 error, re request, error: {str(e)}")
            time.sleep(3)
            res = self.myrequests_get(url, headers=headers, verify=verify)

        while res.status_code != 200:
            # dm3u8.warning(f"【{res.status_code}】request 【{url}】 error, re request")
            time.sleep(1)
            res = self.myrequests_get(url, headers=headers, verify=verify)
        return res

    def get_m3u8_data(self):
        # headers = {
        #     'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        # }
        res = self.myrequests_get(self.m3u8_url)
        m3u8_data = res.text
        if "#EXTM3U" not in m3u8_data:
            raise BaseException("非M3U8的链接")

        m3u8_data = m3u8.loads(m3u8_data).data
        segments = m3u8_data.get('segments')
        return segments

    def download_ts(self, urlprefix, segment, savepath):
        try:
            ts_uri = segment.get('uri')
            # key_method = segment.get('key').get('method')
            key_uri = segment.get('key').get('uri')
            # key_url = urlprefix + key_uri
            # print(key_url)
            key_iv = segment.get('key').get('iv')
            key_iv = key_iv.replace("0x", "")[:16].encode()  # 偏移码
        except Exception as e:
            dm3u8.error(f"{e}, {segment}")
            key = None

        time.sleep(10)

        if not os.path.exists(savepath):
            os.makedirs(savepath)

        if key_uri:  # AES 解密
            ts_url = urlprefix + ts_uri
            file = os.path.join(savepath, ts_uri)
            res = self.myrequests_get(ts_url).content  # 获取视频内容

            try:
                key = self.myrequests_get(key_uri).content
                cryptor = AES.new(key, AES.MODE_CBC, key_iv)
                with open(file, 'wb') as f:
                    f.write(cryptor.decrypt(res))
            except Exception as e:
                dm3u8.warning(f"{e}, segment: {segment}")
                self.download_ts(urlprefix, segment, savepath)

        else:
            with open(file, 'wb') as f:
                f.write(res)

    def main(self, urlprefix, savepath):
        segments = self.get_m3u8_data()
        segments_num = len(segments)
        with ThreadPoolExecutor(max_workers=1) as threadpool:
            list(tqdm(threadpool.map(self.download_ts, [urlprefix]*segments_num, segments, [savepath]*segments_num),
                 total=segments_num, ncols=80, desc=f"[{savepath}](ts下载)"))



if __name__ == '__main__':
    m3u8_url = 'https://testcdn.dkmeco.com/bb93164b22d246d0b1ccaff318218838/04c37fa2648d1bfb7f264d2f276c04ce-sd-encrypt-stream.m3u8'
    urlprefix = 'https://testcdn.dkmeco.com/bb93164b22d246d0b1ccaff318218838/'
    savepath = './test'
    d38 = DownloadM3U8(m3u8_url)
    segments = d38.get_m3u8_data()
    segment = segments[0]
    print(segment)
    d38.download_ts(urlprefix, segment, savepath)


#         def merge_ts2mp4(title):
#             temppath = os.path.join(TARGETPATH, title)
#             temppath = temppath.replace('/', '\\')  # 后续用户合并，使用windows命令，必须这样处理
#             targetpath = os.path.join(TARGETPATH, f'{title}.mp4')
#             targetpath = targetpath.replace('/', '\\')  # 后续用户合并，使用windows命令，必须这样处理
#             subresult = subprocess.run(["copy", "/b", f"{os.path.join(temppath, '*.ts')}", f"{targetpath}"],
#                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

#             if not os.path.isfile(targetpath):
#                 dlogger.warning(f"stdin: {subresult.args}, stderr: {subresult.stderr}")
#             else:
#                 shutil.rmtree(temppath)

#         title = pageinfo.get('title')
#         temppath = os.path.join(TARGETPATH, title)
#         # 生成ts临时文件夹
#         if not os.path.exists(temppath):
#             os.mkdir(temppath)

#         m3u8_url = pageinfo.get('video_m3u8')
#         m3u8_data = get_m3u8_data(m3u8_url)
#         m3u8_data = m3u8.loads(m3u8_data).data
#         segments = m3u8_data.get('segments')
#         segments_num = len(segments)
        
#         with ThreadPoolExecutor(max_workers=60) as threadpool:
#             list(tqdm(threadpool.map(download_ts, [m3u8_url]*segments_num, range(segments_num), 
#                       segments, [temppath]*segments_num),
#                  total=segments_num, ncols=80, desc=f"[{title}](ts下载)"))

#         merge_ts2mp4(title)