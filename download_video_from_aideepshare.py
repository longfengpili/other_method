#!/usr/bin/env python
# coding: utf-8


import requests
from mysetting import *
import json
import os
from bs4 import BeautifulSoup
import time
import sqlite3
import win32crypt


def get_headers(headers):
    username = os.environ.get('USERNAME')[:5]
    cookie_file = f'C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default/Cookies'
    conn = sqlite3.connect(cookie_file)
    cursor = conn.cursor()
    sql = "SELECT encrypted_value FROM cookies where host_key = 'ai.deepshare.net' and name = 'pc_user_key';"
    cursor.execute(sql)
    results = cursor.fetchone()
    conn.close()
    if not results:
        raise ValueError(f'no cookie!{results}')
    pc_user_key = win32crypt.CryptUnprotectData(results[0], None, None, None, 0)[1].decode('utf-8')#解密

    headers['Cookie'] = headers['Cookie'].replace('$pc_user_key', pc_user_key)
    return headers

def get_goods_id(goods_url):
    goods_id_all = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }

    req = requests.get(goods_url, headers=headers)
    soup = BeautifulSoup(req.text)
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
            print(result)
    return goods_id_all

def get_videoslist_from_local(dirpath):
    return os.listdir(dirpath)

def get_info_from_api(api, headers, params, data):
    req = None
    try:
        req = requests.post(api, headers=headers, params=params, data=data)
        req = json.loads(req.text)
    except Exception as e:
        print(f'【9】{e}\n{req}')
        while not req:
            req = get_info_from_api(api, headers, params, data)

    return req

def parse_goodslist(req):
    goods_list = []
    last_id = None
    id = 1
    try:
        goodslist = req.get('data').get('goods_list')
#         print(goodslist)
        last_id = req.get('data').get('last_id')
    except Exception as e:
        print(f'【24】{e}\n{req}')

    if goodslist:
        selection = ['resource_id', 'resource_type', 'title', 'redirect_url']
        for good in goodslist:
            id += 1
            selection_info = [good.get(key) for key in selection]
#             selection_info = [good.get(key) for key in selection if good.get('video_length', 0) > 0]
            if selection_info:
                good = dict(zip(selection, selection_info))
                goods_list.append(good)

    return goods_list, last_id


def get_goodslist(url, headers, app_id, data):
    params = {'app_id': f'{app_id}'}
    goods_list_all = []
    req = get_info_from_api(url, headers, params, data)
#     print(req)
    goods_list, last_id = parse_goodslist(req)
    goods_list_all.extend(goods_list)

    while goods_list:
        data = json.loads(data)
        data['last_id'] = last_id
        data['order_type'] = 0
        data = json.dumps(data)
        req = get_info_from_api(url, headers, params, data)
        goods_list, last_id = parse_goodslist(req)
        goods_list_all.extend(goods_list)

#     if not goods_list_all: print(req)

    return goods_list_all

def get_video(url, headers, good, app_id):
#     print(url)
    params = {'app_id': f'{app_id}'}
    data = {}
    data['goods_id'] = good.get('resource_id')
    data['goods_type'] = good.get('resource_type')
    data = json.dumps(data)
    req_info = get_info_from_api(url, headers, params, data)
#     print(req_info)
    video_info = req_info.get('data')
    return video_info

def download_video(video_info, dirpath, title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    m3u8_url = video_info.get('video_m3u8')
    if m3u8_url:
        name = f"{dirpath}/{title}.mp4"
        try:
            shell_command = f"ffmpeg -i {m3u8_url} -c copy {name}"
            os.system(shell_command)
        except Exception as e:
            print(e)
            print(shell_command)

def save_description(video_info, dirpath, title):
    content = video_info.get('content')
    with open(f'{dirpath}/{title}.html', 'w', encoding='utf-8') as f:
        f.write(content)



if __name__ == '__main__':
    headers = get_headers(headers)
    goods_id_all = get_goods_id(goods_url)
    for title, data in goods_id_all.items():
        print(f"开始下载【{title}】".center(50,'='))
        dirpath = 'f:/深度之眼/' + title
        try:
            os.mkdir(dirpath)
            print(f'{dirpath}已经创建！')
        except Exception as e:
            if '当文件已存在时' not in str(e):
                print(f'【{dirpath}】{e}！')
        goods_list = get_goodslist(main_api, headers, app_id, data)
        for good in goods_list:
    #         print(good)
            video = get_video(page_api, headers, good, app_id)
            if video:
    #             print(video)
                if 'title' in video:
                    title = video.get('title').replace('|', ',').replace(' ','')
                    if f'{title}.html' not in get_videoslist_from_local(dirpath):
                        print(f'【下载】{title}')
                        download_video(video, dirpath, title)
                        time.sleep(1)
                        save_description(video, dirpath, title)
                    else:
        #                 print(f'【已存在】{title}')
                        pass
                else:
                    print(video)

    # os.system('shutdown -s -t 60')





