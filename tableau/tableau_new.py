# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2022-01-05 07:02:14
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-01-06 08:46:47


import os
import json
import time
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

import m3u8
from Crypto.Cipher import AES

from mysetting import DOMAIN, APP_ID, HEADERS, COURSESAPI, COURSEAPI
from chrome_cookie import GetCooikiesFromChrome


class Tableau:

    def __init__(self, app_id, domain, headers, coursesapi, courseapi):
        self.app_id = app_id
        self.domain = domain
        self.headers = headers
        self.coursesapi = coursesapi
        self.courseapi = courseapi

    def create_headers(self):
        get_cookies = GetCooikiesFromChrome()
        cookie = get_cookies.get(self.domain)
        if not cookie:
            raise ValueError("please login")

        self.headers['Cookie'] = cookie
        # dslogger.info(headers)
        return self.headers

    def get_courseslist(self):
        data = '{"page_size":20,"goods_id":"term_61c55f79648f9_RYHNiw","last_id":"","goods_type":25,"resource_type":[6],"has_buy":null}'
        headers = self.create_headers()
        res = requests.post(self.coursesapi, headers=headers, data=data)
        res_json = res.json()
        with open('./goods.json', 'w', encoding='utf-8') as f:
            json.dump(res_json, f)
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
        # print(data)
        headers = self.create_headers()
        res = requests.post(self.coursesapi, headers=headers, data=data)
        res_json = res.json()
        courseinfo = res_json.get('data').get('goods_list')
        return courseinfo

    def get_pageinfo(self, courseinfo):
        data = {}
        data['goods_id'] = courseinfo.get('node_id')
        data['goods_type'] = courseinfo.get('resource_type')

        data = json.dumps(data)
        # print(data)
        headers = self.create_headers()
        res = requests.post(self.courseapi, headers=headers, data=data)
        res_json = res.json()
        pageinfo = res_json.get('data')
        with open('./goods.json', 'w', encoding='utf-8') as f:
            json.dump(pageinfo, f)
        return pageinfo

    def download_video(self, pageinfo):
        def create_video_headers():
            video_headers = {}
            video_headers['host'] = 'encrypt-k-vod.xet.tech'
            headers = self.create_headers()
            video_headers['referer'] = headers['referer']
            video_headers['user-agent'] = headers['user-agent']
            return video_headers

        def myrequests(url, video_headers=None):
            try:
                req = requests.get(url, headers=video_headers, timeout=60) 
            except Exception as e:
                print(f"request 【{url}】 error, re request, error: {str(e)[:100]}")
                time.sleep(3)
                req = myrequests(url)

            while req.status_code != 200:
                print(f"【{req.status_code}】request 【{url}】 error, re request")
                time.sleep(1)
                req = myrequests(url)
            return req

        def get_m3u8_data(m3u8_url, video_headers):
            res = myrequests(m3u8_url, video_headers)
            m3u8_data = res.text
            if "#EXTM3U" not in m3u8_data:
                raise BaseException("非M3U8的链接")
            return m3u8_data

        def download_ts(url_prefix, id, segment):
            '''
            temppath/url_prefix 来自上一层函数
            '''
            # dslogger.warning(f"segment: {segment}")
            temppath = './test'
            file_tmp = os.path.join(temppath, f"{id:0>4d}.ts")
            try:
                key_method = segment.get('key').get('method')
                key_url = segment.get('key').get('uri')
                key = myrequests(key_url).content
                key_iv = segment.get('key').get('iv')
                print(key_iv)
                # key_iv = key_iv.replace("0x", "")[:16].encode()  # 偏移码
                key_iv = '0000000000000000'.encode()
            except:
                key = None
            
            url = url_prefix + segment.get('uri')  # 拼接完整url
            res = myrequests(url).content  # 获取视频内容
            if key:  # AES 解密
                try:
                    cryptor = AES.new(key, AES.MODE_CBC, key_iv)
                    with open(file_tmp, 'wb') as f:
                        f.write(cryptor.decrypt(res))
                except Exception as e:
                    print(f"{e}, id: {id}, segment: {segment}")
                    download_ts(url_prefix, id, segment)
            else:
                with open(file_tmp, 'wb') as f:
                    f.write(res)

        video_headers = create_video_headers()
        m3u8_url = pageinfo.get('video_m3u8')
        url_prefix = m3u8_url.split('drm')[0] + 'drm/' if 'drm/' in m3u8_url else m3u8_url.split('v.f')[0]
        m3u8_data = get_m3u8_data(m3u8_url, video_headers)
        m3u8_data = m3u8.loads(m3u8_data).data
        segments = m3u8_data.get('segments')
        segments_num = len(segments)
        for idx, segment in enumerate(segments):
            download_ts(url_prefix, idx, segment)

        # with ThreadPoolExecutor(max_workers=60) as threadpool:
        #     list(tqdm(threadpool.map(download_ts, [url_prefix]*segments_num, range(segments_num), segments),
        #          total=segments_num, ncols=80, desc="[视频下载]"))

        # # 读线程下载ts
        # url_prefix = url.split('drm')[0] + 'drm/' if 'drm/' in url else url.split('v.f')[0]
        # segments_num = len(segments)
        # # dslogger.info(f"The course have {segments_num} ts！")
        # with ThreadPoolExecutor(max_workers=60) as threadpool:
        #     list(tqdm(threadpool.map(download_ts, range(segments_num), segments),
        #                 total=segments_num, ncols=80, desc="[视频下载]"))

        # # 合并并删除临时文件夹
        # subresult = subprocess.run(["copy", "/b", f"{os.path.join(temppath, '*.ts')}", f"{filepath}"],
        #                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # if not os.path.isfile(filepath):
        #     dslogger.error(f"stdin: {subresult.args}, stderr: {subresult.stderr}")
        #     result = False
        # else:
        #     shutil.rmtree(temppath)

        # et = time.time()
        # dslogger.debug(f">>>>>>视频<<<<<<, 用时{et-st:.2f}秒")




if __name__ == '__main__':
    tableau = Tableau(APP_ID, DOMAIN, HEADERS, COURSESAPI, COURSEAPI)
    courseslist = tableau.get_courseslist()
    course = courseslist[0]
    courseinfo = tableau.get_courseinfo(course)
    pageinfo = tableau.get_pageinfo(courseinfo[0])
    res = tableau.download_video(pageinfo)
    print(res)
    

    
