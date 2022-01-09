# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2022-01-05 07:02:14
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-01-10 07:44:43


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

from mysetting import DOMAIN, APP_ID, HEADERS, COURSEAPI, PAGEAPI, COURSEDATA
from chrome_cookie import GetCooikiesFromChrome

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
dlogger = logging.getLogger(__name__)
dlogger.addHandler(handler)
dlogger.setLevel(logging.DEBUG)


TARGETPATH = r'F:\深度之眼\tableau'


class XiaoE:

    def __init__(self, app_id, domain, headers, courseapi, pageapi):
        self.app_id = app_id
        self.domain = domain
        self.headers = headers
        self.courseapi = courseapi
        self.pageapi = pageapi
        self.cookie = self._get_cookie()
        self._check_targetpath()

    def _check_targetpath(self):
        if not os.path.exists(TARGETPATH):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{TARGETPATH}', please change Variable 'TARGETPATH'")

    def _get_cookie(self):
        get_cookies = GetCooikiesFromChrome()
        cookie = get_cookies.get(self.domain)
        return cookie

    def create_headers(self):
        if not self.cookie:
            raise ValueError("please login")

        self.headers['Cookie'] = self.cookie
        return self.headers

    def myrequests_get(self, url, headers=None):
        try:
            req = requests.get(url, headers=headers, timeout=60) 
        except Exception as e:
            dlogger.error(f"request 【{url}】 error, re request, error: {str(e)[:100]}")
            time.sleep(3)
            req = self.myrequests_get(url, headers=headers)

        while req.status_code != 200:
            # dlogger.warning(f"【{req.status_code}】request 【{url}】 error, re request")
            time.sleep(1)
            req = self.myrequests_get(url, headers=headers)
        return req

    def get_courseslist(self, coursedata):
        headers = self.create_headers()
        res = requests.post(self.courseapi, headers=headers, data=coursedata)
        res_json = res.json()
        # with open('./goods.json', 'w', encoding='utf-8') as f:
        #     json.dump(res_json, f)
        courseslist = res_json.get('data').get('goods_list')
        return courseslist

    def get_courseinfo(self, course):
        data = {}
        data['page_size'] = 20
        data['goods_id'] = course.get('term_id')
        data['goods_type'] = 25
        data['resource_type'] = [1, 2, 3, 4, 20]
        data['node_id'] = course.get('node_id')
        data['type'] = 1
        data['order_type'] = 0
        data = json.dumps(data)
        # dlogger.info(data)
        headers = self.create_headers()
        res = requests.post(self.courseapi, headers=headers, data=data)
        res_json = res.json()
        courseinfo = res_json.get('data').get('goods_list')
        return courseinfo

    def get_pageinfo(self, courseinfo):
        data = {}
        data['goods_id'] = courseinfo.get('node_id')
        data['goods_type'] = courseinfo.get('resource_type')

        data = json.dumps(data)
        # dlogger.info(data)
        headers = self.create_headers()
        res = requests.post(self.pageapi, headers=headers, data=data)
        res_json = res.json()
        pageinfo = res_json.get('data')
        return pageinfo

    def download_html(self, pageinfo):
        title = pageinfo.get('title')
        pagecontent = pageinfo.get('content')
        with open(f'{TARGETPATH}/{title}.html', 'w', encoding='utf-8') as f:
            f.write(pagecontent)

    def download_video(self, pageinfo):
        def create_video_headers():
            video_headers = {}
            video_headers['host'] = 'encrypt-k-vod.xet.tech'
            headers = self.create_headers()
            video_headers['referer'] = headers['referer']
            video_headers['user-agent'] = headers['user-agent']
            return video_headers

        def get_m3u8_data(m3u8_url):
            video_headers = create_video_headers()
            res = self.myrequests_get(m3u8_url, video_headers)
            m3u8_data = res.text
            if "#EXTM3U" not in m3u8_data:
                raise BaseException("非M3U8的链接")
            return m3u8_data

        def download_ts(m3u8_url, id, segment, temppath):
            url_prefix = m3u8_url.split('drm')[0] + 'drm/' if 'drm/' in m3u8_url else m3u8_url.split('v.f')[0]
            video_headers = create_video_headers()
            file_tmp = os.path.join(temppath, f"{id:0>4d}.ts")
            try:
                # key_method = segment.get('key').get('method')
                key_url = segment.get('key').get('uri')
                key = self.myrequests_get(key_url).content
                key_iv = segment.get('key').get('iv')
                key_iv = key_iv.replace("0x", "")[:16].encode()  # 偏移码
            except Exception as e:
                dlogger.error(e)
                key = None
            
            url = url_prefix + segment.get('uri')  # 拼接完整url
            res = self.myrequests_get(url, video_headers).content  # 获取视频内容
            if key:  # AES 解密
                try:
                    cryptor = AES.new(key, AES.MODE_CBC, key_iv)
                    with open(file_tmp, 'wb') as f:
                        f.write(cryptor.decrypt(res))
                except Exception as e:
                    dlogger.warning(f"{e}, id: {id}, segment: {segment}")
                    download_ts(url_prefix, id, segment, temppath)
            else:
                with open(file_tmp, 'wb') as f:
                    f.write(res)

        def merge_ts2mp4(title):
            temppath = os.path.join(TARGETPATH, title)
            temppath = temppath.replace('/', '\\')  # 后续用户合并，使用windows命令，必须这样处理
            targetpath = os.path.join(TARGETPATH, f'{title}.mp4')
            subresult = subprocess.run(["copy", "/b", f"{os.path.join(temppath, '*.ts')}", f"{targetpath}"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            if not os.path.isfile(targetpath):
                dlogger.warning(f"stdin: {subresult.args}, stderr: {subresult.stderr}")
            else:
                shutil.rmtree(temppath)

        title = pageinfo.get('title')
        temppath = os.path.join(TARGETPATH, title)
        # 生成ts临时文件夹
        if not os.path.exists(temppath):
            os.mkdir(temppath)

        m3u8_url = pageinfo.get('video_m3u8')
        m3u8_data = get_m3u8_data(m3u8_url)
        m3u8_data = m3u8.loads(m3u8_data).data
        segments = m3u8_data.get('segments')
        segments_num = len(segments)
        
        with ThreadPoolExecutor(max_workers=60) as threadpool:
            list(tqdm(threadpool.map(download_ts, [m3u8_url]*segments_num, range(segments_num), 
                      segments, [temppath]*segments_num),
                 total=segments_num, ncols=80, desc=f"[{title}](ts下载)"))

        merge_ts2mp4(title)
        
    def download(self, pageinfo):
        self.download_html(pageinfo)
        self.download_video(pageinfo)

    def download_by_course(self, course):
        st = time.time()
        courseinfo = self.get_courseinfo(course)
        if not courseinfo:
            title = course.get('title')
            unlock_time = course.get('unlock_time')
            dlogger.warning(f"【{title}】 lock, unlock_time: {unlock_time} !")
            return

        pageinfo = self.get_pageinfo(courseinfo[0])

        title = pageinfo.get('title')
        targetpath = os.path.join(TARGETPATH, f'{title}.mp4')
        if not os.path.exists(targetpath):
            self.download(pageinfo)
            et = time.time()
            dlogger.info(f"download 【{title}】 cost {et - st:.2f} seconds !")
        else:
            dlogger.info(f"{targetpath} already exists")


if __name__ == '__main__':
    xe = XiaoE(APP_ID, DOMAIN, HEADERS, COURSEAPI, PAGEAPI)
    courseslist = xe.get_courseslist(COURSEDATA)
    for course in courseslist:
        courseinfo = xe.download_by_course(course)
