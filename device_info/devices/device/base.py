# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 13:39:07
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-17 17:30:03
# @github: https://github.com/longfengpili


import time
import random
import threading
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from lxml.etree import Element as elem

from devices.parser import Phone
from devices.parser import Parser
from devices.requester import Requester

import logging
pblogger = logging.getLogger(__name__)


class PhoneBase(Requester, Parser):
    pblock = threading.Lock()

    def __init__(self, kind_path: str, pkind_selector: str, kind_mpaths: tuple[tuple[str, tuple[str]]]):
        self.kind_path = kind_path
        self.kind_mpaths = kind_mpaths
        self.pkind_selector = pkind_selector
        super(PhoneBase, self).__init__()

    def request(self, pname: str):
        pass

    def get_pkinds(self, pname: str):
        url, res = self.request(pname)
        res = res.text
        html = self.etree_html(res)
        # main page
        pkinds = self.get_elem(html, self.kind_path)
        return url, pkinds

    def parse_pkind(self, pkind: elem):
        pkind = self.get_elem_mpath(pkind, *self.kind_mpaths)
        purl = pkind['purl']
        purl_netloc = urlparse(purl).netloc
        if not purl_netloc:
            pkind['purl'] = self.base_url + purl
        return pkind

    def get_phone_by_pkind(self, pkind: elem):
        phone = {}
        phone.update(pkind)
        time.sleep(random.random() * 5)
        purl = pkind.get('purl')
        res, status_code = self.base_request(purl)
        res = res.text
        # with open('./test.html', 'w', encoding='utf-8') as f:
        #     f.write(res)
        phone = self.etree_html(res)

        return phone
        
    def parse_phone(self, phone: elem):
        pass

    def get_phone(self, idx: int, pname: str):
        pkind_selector = self.pkind_selector
        phone_info = []

        pblogger.info(f"【START】, [{idx:0>4d}]{pname}, pkind select [{self.pkind_selector}] ~")
        url, pkinds = self.get_pkinds(pname)

        if pkind_selector == 'first':
            pkinds = pkinds[:1]
        elif pkind_selector == 'random':
            pkinds = random.sample(pkinds, 1)
        else:
            pass

        pklength = len(pkinds)
        for pkidx, pkind in enumerate(pkinds):
            pkind = self.parse_pkind(pkind)

            phone = self.get_phone_by_pkind(pkind)
            phone = self.parse_phone(phone)

            pkidx = None if pklength == 1 else pkidx
            mphone = Phone(idx=idx, surl=url, pkidx=pkidx, pname=pname, **pkind, **phone)
            pblogger.debug(mphone)
            phone_info.append(mphone)
        
        if pklength == 0:  # 解决没有pkinds的数据
            mphone = Phone(idx=idx, surl=url, pname=pname)
            pblogger.debug(mphone)
            phone_info.append(mphone)

        phone_info = Phone.concat(*phone_info)
        pblogger.info(f"【END】, [{idx:0>4d}]{pname} ~")
        phone_info.dump()
        return phone_info

    def get_phones_with_tpool(self, phones: list, max_workers: int = 5):
        thread_name_prefix = f"p{max_workers}"
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix) as tpool:
            phones = tpool.map(self.get_phone, range(len(phones)), phones)

        return phones
