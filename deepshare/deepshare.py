# @Author: chunyang.xu
# @Date:   2020-05-10 07:36:24
# @Last Modified by:   longf
# @Last Modified time: 2020-05-10 14:18:50

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from mysetting import *
import json
import os
from bs4 import BeautifulSoup
import time
import sqlite3
import datetime
import requests
from Crypto.Cipher import AES
import m3u8
import sys
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tqdm import tqdm

import colorlog
log_colors_config = {
    # 'DEBUG': 'cyan',
    # 'INFO': 'yellow',
    'WARNING': 'red',
    'ERROR': 'red, bg_white',
    'CRITICAL': 'red, bg_white',
}
formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(log_color)s%(message)s',
            log_colors=log_colors_config)

import logging
handler = logging.StreamHandler()
handler.setFormatter(formatter)
dslogger = logging.getLogger('deepshare')
dslogger.addHandler(handler)
dslogger.setLevel(logging.INFO)

class GetCooikiesFromChrome(object):
    '''[summary]
        Chrome 80.X版本解密Cookies文件
    [description]
    '''

    def __init__(self):
        pass

    def dpapi_decrypt(self, encrypted):
        import ctypes
        import ctypes.wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [('cbData', ctypes.wintypes.DWORD),
                        ('pbData', ctypes.POINTER(ctypes.c_char))]

        p = ctypes.create_string_buffer(encrypted, len(encrypted))
        blobin = DATA_BLOB(ctypes.sizeof(p), p)
        blobout = DATA_BLOB()
        retval = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
        if not retval:
            raise ctypes.WinError()
        result = ctypes.string_at(blobout.pbData, blobout.cbData)
        ctypes.windll.kernel32.LocalFree(blobout.pbData)
        return result

    def aes_decrypt(self, encrypted_txt):
        with open(os.path.join(os.environ['LOCALAPPDATA'],
                               r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
            jsn = json.loads(str(f.readline()))
        encoded_key = jsn["os_crypt"]["encrypted_key"]
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_key = encrypted_key[5:]
        key = self.dpapi_decrypt(encrypted_key)
        nonce = encrypted_txt[3:15]
        cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
        cipher.mode = modes.GCM(nonce)
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_txt[15:])

    def chrome_decrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'x01x00x00x00':
                    decrypted_txt = self.dpapi_decrypt(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = self.aes_decrypt(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            raise WindowsError

    def get(self, domain):
        sql = f'SELECT name, encrypted_value as value FROM cookies where host_key like "%{domain}%"'
        filename = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\default\Cookies')
        con = sqlite3.connect(filename)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        
        cookie = ''
        for row in cur:
            if row['value'] is not None:
                name = row['name']
                value = self.chrome_decrypt(row['value'])
                if value is not None:
                    cookie += name + '=' + value + ';'
        con.close()
        cookie = cookie.encode('utf-8')
        if not cookie:
            raise f"cookie is not exist! {cookie}"
        return cookie



class DeepShare(object):
    def __init__(self, app_id):
        self.courseslist = None
        self.app_id = app_id

    def create_headers(self, headers):
        '''[summary]
            生成带cookies的headers
        [description]
        
        Arguments:
            headers {[dict]} -- [不带cookie的默认内容]
        
        Returns:
            [dict] -- [带cookies的headers]
        '''
        get_cookies = GetCooikiesFromChrome()
        cookie = get_cookies.get('ai.deepshare.net')
        if not cookie:
            dslogger.warning('please login')
        headers['Cookie'] = cookie
        # dslogger.info(headers)
        return headers

    def get_goods_id(self, goods_url, headers_agent):
        '''[summary]
        获取所有课程id
        
        [description]
        
        Arguments:
            goods_url {[str]} -- [课程总展示页面]
            headers_agent {[dict]} -- [只带有user_agent的headers]
        
        Returns:
            [dict] -- [所有课程信息]
        '''
        goods_id_all = {}
        req = requests.get(goods_url, headers=headers_agent)
        soup = BeautifulSoup(req.text, 'lxml')
        results = soup.find_all(class_="hot-item")
        for result in results:
            try:
                goods_data = {"page_size":20,"last_id":"","resource_type":[1,2,3,4]}
                title = result.div.div.string.strip()
                goods_id, goods_type = result['href'].split('/')[2], result['href'].split('/')[3]
                goods_data['goods_id'] = goods_id
                goods_data['goods_type'] = int(goods_type) if goods_type else 6
                goods_data = json.dumps(goods_data)
                goods_id_all[title] = goods_data
            except:
                dslogger.error(result)
        return goods_id_all

    def get_videoslist_from_local(self, dirpath):
        return os.listdir(dirpath)

    def get_info_from_api(self, api, headers, data):
        '''[summary]
        通过API获取单个课程信息 method:POST
        [description]
        
        Arguments:
            api {[str]} -- [api url]
            headers {[dict]} -- [cookies headers]
            params {[dict]} -- [requests params]
            data {[dict]} -- [requests POST data]
        
        Returns:
            [dict] -- [课程信息]
        '''
        params = {'app_id': f'{self.app_id}'}
        req = None
        try:
            req = requests.post(api, headers=headers, params=params, data=data)
            req = json.loads(req.text)
        except Exception as e:
            dslogger.error(f'{e}\n{req}')
            while not req:
                req = get_info_from_api(api, headers, params, data)
        
        return req

    def get_courseslist(self, main_api, headers, data):
        '''[summary]
        获取单个课程的所有课程列表
        
        [description]
        
        Arguments:
            api {[str]} -- [api url]
            headers {[dict]} -- [cookies headers]
            data {[dict]} -- [requests POST data]
        
        Returns:
            [type] -- [description]
        '''
        req = self.get_info_from_api(main_api, headers, data)

        if self.courseslist is None:
            self.courseslist = []
        last_id = None
        try:
            courses_info = req.get('data').get('goods_list')
            last_id = req.get('data').get('last_id')
        except Exception as e:
            dslogger.error(f'{e}\n{req}')
            
        if courses_info:
            selection = ['resource_id', 'resource_type', 'title', 'redirect_url']
            for course in courses_info:
                selection_info = [course.get(key) for key in selection]
                if selection_info:
                    course = dict(zip(selection, selection_info))
                    self.courseslist.append(course)
            if last_id:
                data = json.loads(data)
                data['last_id'] = last_id
                data['order_type'] = 0
                data = json.dumps(data)
                return self.get_courseslist(main_api, headers, data)
        if self.courseslist:
            dslogger.info(f"This good have {len(self.courseslist)} courses!")
        else:
            dslogger.warning(f"{req}")
        return self.courseslist
    

    def get_course_info(self, page_api, headers, course):
        '''[summary]
        获取单个课程的信息
        
        [description]
        
        Arguments:
            page_api {[str]} -- [单个课程api]
            headers {[dict]} -- [cookies headers]
            course {[dict]} -- [课程信息（简单）]
        
        Returns:
            [dict] -- [课程信息]
        '''
        data = {}
        data['goods_id'] = course.get('resource_id')
        data['goods_type'] = course.get('resource_type')
        data = json.dumps(data)
        req = self.get_info_from_api(page_api, headers, data)
        course_info = req.get('data')
        return course_info

    def download_video(self, course_info, headers_video, dirpath, title):
        '''[summary]
        下载视频
        
        [description]
        
        Arguments:
            course_info {[dict]} -- [课程详细信息]
            headers_video {[dict]} -- [下载视频的headers]
            dirpath {[str]} -- [下载目录]
            title {[str]} -- [视频名]
        
        Returns:
            [type] -- [description]
        '''
        def myrequests(url, headers=headers_video, times=5):
            try_times = 0
            req = requests.get(url, headers=headers)
            while req.status_code != 200 and try_times < times:
                req = requests.get(url, headers=headers)
                try_times += 1
            if req.status_code != 200:
                raise ValueError(f"request error ! 【{try_times}】{url}")
            return req
        
        st = time.time()
        filepath = os.path.join(dirpath, title) + '.mp4'
        try:
            os.remove(filepath) #重新启动下载的话，删除原有下载
        except:
            pass
        
        url = course_info.get('video_m3u8').replace("http", "https")
        if not url:
            return
        url_prefix = url.split('v.f230')[0]

        all_content = myrequests(url).text  # 获取m3u8文件
        if "#EXTM3U" not in all_content:
            raise BaseException("非M3U8的链接")

        m3u8_data = m3u8.loads(all_content).data
        segments = m3u8_data.get('segments')
        if not segments: #如果没有
            dslogger.info(f"{title}\n{all_content}")
            return 

        for segment in tqdm(segments, ncols=80):
            # dslogger.info(f"{segment}")
            try:
                key_method = segment.get('key').get('method')
                key_url = segment.get('key').get('uri')
                key = myrequests(key_url).content
                key_iv = segment.get('key').get('iv')
                key_iv = key_iv.replace("0x", "")[:16].encode()  # 偏移码
            except:
                key = None
                
            url = url_prefix + segment.get('uri') #拼接完整url
            res = myrequests(url).content #获取视频内容
            if key:  # AES 解密
                cryptor = AES.new(key, AES.MODE_CBC, key_iv)
                with open(filepath, 'ab') as f:
                    f.write(cryptor.decrypt(res))
            else:
                with open(filepath, 'ab') as f:
                    f.write(res)
                    f.flush()
        if segments:
            et = time.time()
            dslogger.info(f"视频下载完成,用时{et-st:.2f}秒")
        
    def save_description(self, course_info, dirpath, title):
        content = course_info.get('content')
        with open(f'{dirpath}/{title}.html', 'w', encoding='utf-8') as f:
            f.write(content)

    def download_course(self, page_api, headers, headers_video, course, dirpath):
        course_info = self.get_course_info(page_api, headers, course)
        if course_info:
            try:
                title = course_info.get('title').replace('|', ',').replace(' ','').replace('/','')
                if f'{title}.html' not in self.get_videoslist_from_local(dirpath):
                    dslogger.info(f'【下载】{title}')
                    self.download_video(course_info, headers_video, dirpath, title)
                    time.sleep(1)
                    self.save_description(course_info, dirpath, title)
            except:
                dslogger.error(course_info)


if __name__ == "__main__":
    ds = DeepShare(app_id)
    headers = ds.create_headers(headers)
    goods_id_all = ds.get_goods_id(goods_url, headers_agent)
    for title, data in goods_id_all.items():
        dslogger.info(f"开始下载【{title}】")
        dirpath = os.path.join('f:/深度之眼/', title)
        try:
            os.mkdir(dirpath)
            print(f'{dirpath}已经创建！')
        except Exception as e:
            if '当文件已存在时' not in str(e):
                print(f'【{dirpath}】{e}！')

        ds.courseslist = None #每次重置
        courseslist = ds.get_courseslist(main_api, headers, data)
        for course in courseslist:
            ds.download_course(page_api, headers, headers_video, course, dirpath)
        
        # break

    # os.system('shutdown -s -t 60')




