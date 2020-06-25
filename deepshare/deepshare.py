# @Author: chunyang.xu
# @Date:   2020-05-10 07:36:24
# @Last Modified by:   longf
# @Last Modified time: 2020-06-25 12:05:42

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from mysetting import *
import json
import os
from bs4 import BeautifulSoup
import time
import sqlite3
from datetime import datetime, date
import requests
from Crypto.Cipher import AES
import m3u8
import sys
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import subprocess
import shutil

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

import logging
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handlerfile = logging.FileHandler('./erorr.log', encoding='utf-8')
handlerfile.setFormatter(formatter)
handlerfile.setLevel(logging.ERROR)
dslogger = logging.getLogger('deepshare')
dslogger.addHandler(handler)
dslogger.addHandler(handlerfile)
dslogger.setLevel(logging.DEBUG)



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
        self.app_id = app_id
        self.goods_datas = self.load_json()
        self.title_info = None # 由于有的章节title一致，故统计数量用于区分

    def load_json(self):
        with open('./goods.json', 'rb') as f:
            data = json.load(f)
        return data

    def dump_json(self):
        data = dict(sorted(self.goods_datas.items(), 
                key=lambda x: (x[1].get('nodownload_days', 0), x[1].get('courses_num', 0))))
        with open('./goods.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

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

    def get_goods_datas(self, goods_url, headers_agent):
        '''[summary]
        获取所有课程信息

        [description]

        Arguments:
            goods_url {[str]} -- [课程总展示页面]
            headers_agent {[dict]} -- [只带有user_agent的headers]

        Returns:
            [dict] -- [所有课程信息]
        '''
        req = requests.get(goods_url, headers=headers_agent)
        soup = BeautifulSoup(req.text, 'lxml')
        results = soup.find_all(class_="hot-item")
        for result in results:
            try:
                goods_data = {"page_size":20,"last_id":"","resource_type":[1,2,3,4]}
                title = result.div.div.string.strip().replace('+', '')
                url = 'https://ai.deepshare.net' + result['href']
                goods_data['url'] = url
                goods_id, goods_type = result['href'].split('/')[2], result['href'].split('/')[3]
                goods_data['goods_id'] = goods_id
                goods_data['goods_type'] = int(goods_type) if goods_type else 6
            except:
                dslogger.error(result)

            if title not in self.goods_datas:
                goods_data['create_ts'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                self.goods_datas[title] = goods_data
            else:
                self.goods_datas[title].update(goods_data)
        self.dump_json()
        return self.goods_datas

    def get_filelist_from_local(self, dirpath):
        files = os.listdir(dirpath)
        files_noix = [file[6:] for file in files]
        files_nosuffix = [file[:-5] for file in files if file.endswith('.html')]
        # dslogger.info(files)
        return files, files_noix, files_nosuffix

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
        data = json.dumps(data)
        params = {'app_id': f'{self.app_id}'}
        req = requests.post(api, headers=headers, params=params, data=data)
        while req.status_code != 200:
            req = requests.post(api, headers=headers, params=params, data=data)
        req = json.loads(req.text)

        if req.get('msg') == '立即登录':
            raise Exception(f"请先登陆！")

        return req

    def get_courseslist_once(self, main_api, headers, data):
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
        def convert_title(title):
            title_count = self.title_info.get(title, 0) + 1
            self.title_info[title] = title_count
            title = f"{title}_{title_count:0>2d}" if title_count > 1 else title
            return title

        if not self.title_info:
            self.title_info = {}

        continue_download = False
        courseslist_once = []
        req = self.get_info_from_api(main_api, headers, data)
        courses_list = req.get('data').get('goods_list')
        last_id = req.get('data').get('last_id')
        goods_id = data.get('goods_id')
        goods_type = data.get('goods_type')

        if courses_list:
            selection = ['resource_id', 'resource_type', 'title', 'redirect_url', 'start_at']
            for course in courses_list:
                course = {key: course.get(key) for key in selection}
                course['goods_id'] = goods_id
                course['goods_type'] = goods_type
                course['title'] = convert_title(course['title'])
                courseslist_once.append(course)
        if last_id:
            continue_download = True
            data['last_id'] = last_id
            data['order_type'] = 0

        return continue_download, courseslist_once, data

    def get_courseslist(self, main_api, headers, data, title):
        nodownload_days = self.goods_datas.get(title).get('nodownload_days', 0)
        update_ts_last = self.goods_datas.get(title).get('update_ts', '1987-01-01')
        myupdate_date = self.goods_datas.get(title).get('myupdate_date', '1987-01-01')
        update_ts = None
        today = datetime.strftime(date.today(), '%Y-%m-%d')
        
        courseslist = []
        continue_download, courseslist_once, data = self.get_courseslist_once(main_api, headers, data)
        courseslist.extend(courseslist_once)
        while continue_download:
            continue_download, courseslist_once, data = self.get_courseslist_once(main_api, headers, data)
            courseslist.extend(courseslist_once)
        if courseslist:
            update_ts = courseslist[-1].get('start_at')
            self.goods_datas[title]['update_ts'] = update_ts
            courses_num = len(courseslist)
            self.goods_datas[title]['courses_num'] = courses_num
            last_course_title = courseslist[-1].get('title')
            self.goods_datas[title]['last_course_title'] = last_course_title
            dslogger.info(f"【last_updated: {update_ts}】This Good have {courses_num} courses!")
        
        if not update_ts or update_ts_last == update_ts:
            if myupdate_date != today:
                nodownload_days += 1
                self.goods_datas[title]['nodownload_days'] = nodownload_days
            courseslist = []
        else:
            self.goods_datas[title]['nodownload_days'] = 0

        self.goods_datas[title]['myupdate_date'] = today

        return courseslist


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
        data['from_id'] = course.get('goods_id')
        data['type'] = course.get('goods_type')
        req = self.get_info_from_api(page_api, headers, data)
        course_info = req.get('data')
        # dslogger.error(course_info)
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
        def myrequests(url, headers=headers_video, times=20):
            try_times = 0
            req = requests.get(url, headers=headers, timeout=60)
            while req.status_code != 200 and try_times < times:
                req = requests.get(url, headers=headers, timeout=60)
                try_times += 1
            if req.status_code != 200:
                raise ValueError(f"request error ! 【{try_times}】{url}")
            return req

        def download_ts(id, segment):
            '''
            temppath/url_prefix 来自上一层函数
            '''
            file_tmp = os.path.join(temppath, f"{id:0>4d}.ts")
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
            # dslogger.debug(f"{key_method}, {key}, {key_iv}")
            if key:  # AES 解密
                cryptor = AES.new(key, AES.MODE_CBC, key_iv)
                with open(file_tmp, 'wb') as f:
                    f.write(cryptor.decrypt(res))
            else:
                with open(file_tmp, 'wb') as f:
                    f.write(res)

        result = True
        st = time.time()
        temppath = os.path.join(dirpath, title).replace('/', '\\') #后续用户合并，使用windows命令，必须这样处理
        filepath = temppath + '.mp4'

        url = course_info.get('video_m3u8', '').replace("http", "https")
        if not url: return result

        all_content = myrequests(url).text  # 获取m3u8文件
        if "#EXTM3U" not in all_content:
            raise BaseException("非M3U8的链接")

        m3u8_data = m3u8.loads(all_content).data
        segments = m3u8_data.get('segments')
        if not segments: #如果没有
            dslogger.info(f"{title}\n{all_content}")
            result = False
            return result

        # 生成ts临时文件夹
        if not os.path.exists(temppath):
            os.mkdir(temppath)

        # 读线程下载ts
        url_prefix = url.split('v.f230')[0]
        segments_num = len(segments)
        # dslogger.info(f"The course have {segments_num} ts！")
        with ThreadPoolExecutor(max_workers=60) as threadpool:
            list(tqdm(threadpool.map(download_ts, range(segments_num), segments),
                        total=segments_num, ncols=80, desc="[视频下载]"))

        # 合并并删除临时文件夹
        subresult = subprocess.run(["copy", "/b", f"{os.path.join(temppath, '*.ts')}", f"{filepath}"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if not os.path.isfile(filepath):
            dslogger.error(f"stdin: {subresult.args}, stderr: {subresult.stderr}")
            result = False
        else:
            shutil.rmtree(temppath)

        et = time.time()
        dslogger.debug(f">>>>>>视频<<<<<<, 用时{et-st:.2f}秒")

        return result

    def save_description(self, course_info, dirpath, title):
        content = course_info.get('content', '')
        if not content:
            title = title + '[empty]' 
        with open(f'{dirpath}/{title}.html', 'w', encoding='utf-8') as f:
            f.write(content)
        dslogger.debug(f">>>>>>网页<<<<<<")

    def download_course(self, index, page_api, headers, headers_video, course, dirpath):
        def rename_file(dirpath, oldfile, newfile):
            oldfile = os.path.join(dirpath, oldfile)
            newfile = os.path.join(dirpath, newfile)
            try:
                os.rename(oldfile, newfile)
                dslogger.debug(f"【RENAME】{oldfile} rename to {newfile}")
            except Exception as e:
                dslogger.warning(f"{e}")

        files, files_noix, files_nosuffix = self.get_filelist_from_local(dirpath)

        title_noix = course.get('title', None)
        trips = '<>/\|:"*? +-&,'
        for t in trips:
            title_noix = title_noix.replace(t, '_') 
        title = f"【{index:0>4d}】{title_noix}"

        course_info = self.get_course_info(page_api, headers, course)

        if not title_noix or not course_info:
            raise ValueError(f"{course}")

        if f"{title}.html" not in files and f"{title_noix}.mp4" in files_noix:
            oldfiles = [file for file in files_nosuffix 
                            if f'{title_noix}' == file or f'{title_noix}' == file + '[empty]']
            oldfiles = [file for select in oldfiles for file in files if select == file]
            for file in oldfiles:
                rename_file(dirpath, file, f"{title}.{file.split('.')[-1]}")

        if f"{title_noix}.mp4" not in files_noix:
            result = self.download_video(course_info, headers_video, dirpath, title)
            while not result:
                dslogger.warning(f"重新下载【{title}.mp4】")
                result = self.download_video(course_info, headers_video, dirpath, title)
            oldfiles = [file for file in files_nosuffix if f'【{index:0>4d}】' in file 
                            and title != file and title != file + '[empty]'] #非本堂课程
            oldfiles = [file for select in oldfiles for file in files if select == file]
            # print(title, oldfiles)
            for file in oldfiles:
                rename_file(dirpath, file, f'【0000】{file[6:]}')

        if f"{title}.html" not in files and f"{title}[empty].html" not in files:
            self.save_description(course_info, dirpath, title)

if __name__ == "__main__":
    ds = DeepShare(app_id)
    headers = ds.create_headers(headers)
    goods_datas = ds.get_goods_datas(goods_url, headers_agent)
    # dslogger.info(goods_datas)

    for title, data in goods_datas.items():
        ds = DeepShare(app_id) # 每次初始化
        nodownload_days = data.get('nodownload_days', 0)
        courses_num = data.get('courses_num', 0)
        if nodownload_days >= 14 and courses_num >= 10: #14次查询没有更新课程，并且课程大于10
            continue
        dslogger.info(f"开始下载【{title}】".center(60, '='))
        dirpath = os.path.join('f:/深度之眼/', title)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
            print(f'{dirpath}已经创建！')
 
        courseslist = ds.get_courseslist(main_api, headers, data, title)
        # dslogger.error(courseslist)
        # print(sorted(ds.title_info.items(), key=lambda x: x[1], reverse=True))
        for ix, course in enumerate(courseslist):
            ix += 1
            # print(course)
            # break
            dslogger.info(f'【下载({ix}/{len(courseslist)})】{course.get("title")[:20]}...')
            ds.download_course(ix, page_api, headers, headers_video, course, dirpath)
        ds.dump_json()


    # os.system('shutdown -s -t 60')




