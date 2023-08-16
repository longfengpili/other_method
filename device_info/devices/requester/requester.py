# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 14:18:08
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-16 11:46:52
# @github: https://github.com/longfengpili

import requests

import logging
glogger = logging.getLogger(__name__)


class Requester:

    def __init__(self):
        pass

    @property
    def base_url(self):
        base_url = ''
        return base_url

    @property
    def headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        return headers

    def base_request(self, url: str, params: dict = None, try_times: int = 4):
        headers = self.headers
        res = requests.get(url, headers=headers, params=params)
        status_code = res.status_code
        while status_code != 200 and try_times > 0:
            glogger.warning(f"[Error: {status_code}]Get {url} !")
            res = requests.get(url, headers=headers, params=params)
            status_code = res.status_code
            try_times -= 1

        res = res.text if status_code == 200 else ''
        return res
