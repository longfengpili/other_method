# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 13:39:07
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 16:09:54
# @github: https://github.com/longfengpili


import time
import random

from urllib.parse import urlparse
from lxml.etree import Element as elem

from devices.parser import Phone
from devices.parser import Parser
from devices.requester import Requester

import logging
pblogger = logging.getLogger(__name__)


class PhoneBase(Requester, Parser):

    def __init__(self, kind_path: str, pkind_selector: str, kind_mpaths: tuple[tuple[str, tuple[str]]]):
        self.kind_path = kind_path
        self.kind_mpaths = kind_mpaths
        self.pkind_selector = pkind_selector
        super(PhoneBase, self).__init__()

    def request(self, pname: str):
        pass

    def get_pkinds(self, pname: str):
        res = self.request(pname)
        html = self.etree_html(res)
        # main page
        pkinds = self.get_elem(html, self.kind_path)
        return pkinds

    def parse_pkind(self, pkind: elem):
        pkind = self.get_elem_mpath(pkind, *self.kind_mpaths)
        purl = pkind['purl']
        purl_netloc = urlparse(purl).netloc
        if not purl_netloc:
            pkind['purl'] = self.base_url + purl
        return pkind

    def get_phone(self, pkind: elem):
        phone = {}
        phone.update(pkind)
        time.sleep(random.random() * 5)
        purl = pkind.get('purl')
        res = self.base_request(purl)
        # with open('./test.html', 'w', encoding='utf-8') as f:
        #     f.write(res)
        phone = self.etree_html(res)

        return phone
        
    def parse_phone(self, phone: elem):
        pass

    def get_phones(self, phones: list, fidx: int = 0):
        pkind_selector = self.pkind_selector

        for idx, pname in enumerate(phones):
            idx += fidx
            pblogger.info(f"Get [{idx:0>4d}]{pname} start, pkind select {self.pkind_selector} ~")
            pkinds = self.get_pkinds(pname)

            if pkind_selector == 'first':
                pkinds = pkinds[:1]
            elif pkind_selector == 'random':
                pkinds = random.sample(pkinds, 1)
            else:
                pass

            for pkidx, pkind in enumerate(pkinds):
                phone_info = {}
                pkind = self.parse_pkind(pkind)
                phone_info.update(pkind)

                phone = self.get_phone(pkind)
                phone = self.parse_phone(phone)
                phone_info.update(phone)

                phone_info['idx'] = f"{idx:0>4d}::{pname}::{pkidx:0>4d}"
                phone_info['pname'] = pname
                mphone = Phone.load(phone_info)
                pblogger.info(mphone)
                print(phone_info)
