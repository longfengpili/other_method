# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-06-16 09:17:10
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-11 11:40:21


import time
import random
import json
import cloudscraper
from lxml import etree

import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
# LOGGING_CONFIG['handlers']['console']['formatter'] = 'color'
logging.config.dictConfig(LOGGING_CONFIG)
klogger = logging.getLogger(__name__)


class GetPhoneInfo:

    def __init__(self):
        pass

    def create_scraper(self):
        if not hasattr(GetPhoneInfo, 'scraper'):
            GetPhoneInfo.scraper = cloudscraper.create_scraper()
        return GetPhoneInfo.scraper

    def get_page(self, url: str):
        scraper = self.create_scraper()
        res = scraper.get(url)
        res = res.text
        return res

    def get_element_info(self, element: etree.Element, path: str, isfirst: bool = True):
        info = element.xpath(path)
        if not info:
            info = 'unknown'
        elif isfirst:
            info = info[0]
        else:
            info = '||'.join([i.strip() for i in info])
        return info

    def get_phone_kinds(self, idxname: str = None, pname: str = None, page: int = None):
        pkinds = []
        base_url = 'https://www.kimovil.com/en/compare-smartphones/'
        _url_param = f'name.{pname}' if pname else f'page.{page}'
        url = base_url + _url_param
        res = self.get_page(url)
        # print(url)
        html = etree.HTML(res)
        phones = html.xpath('//div[@class="item-wrap"]')
        for idx, phone in enumerate(phones):
            phone_info = {}
            phone_info['idx'] = f'{idxname}_{idx}' if idxname else idx
            phone_info['idx_name'] = pname
            phone_info['pname'] = self.get_element_info(phone, './/div[@class="title"]/text()')
            phone_info['purl'] = self.get_element_info(phone, './/a[@class="device-link"]/@href')
            phone_info['prelease'] = self.get_element_info(phone, './/div[@class="status available"]/text()')
            pkinds.append(phone_info)

        return pkinds

    def get_phone_info(self, pkind: dict):
        phone = {}
        phone.update(pkind)
        time.sleep(random.random() * 5)
        purl = pkind.get('purl')
        res = self.get_page(purl)
        html = etree.HTML(res)
        phone_info = html.xpath('//ul[@class="kiui-grid k-main k-auto-column device-mini-datasheet device-mini-datasheet-sheet"]')[0]  # noqa: E501
        phone['screen'] = self.get_element_info(phone_info, './/li[@class="item item-screen k-rowspan-2"]/*/span/text()', isfirst=False)
        phone['size'] = self.get_element_info(phone_info, './/li[@class="item item-size k-rowspan-2"]/*/span/text()', isfirst=False)
        phone['soc'] = self.get_element_info(phone_info, './/li[@class="item item-soc k-rowspan-2"]/*/span/text()', isfirst=False)
        phone['antutu'] = self.get_element_info(phone_info, './/li[@class="item item-antutu"]/*/span/text()', isfirst=False)
        phone['battery'] = self.get_element_info(phone_info, './/li[@class="item item-battery"]/*/span/text()', isfirst=False)
        phone['os'] = self.get_element_info(phone_info, './/li[@class="item item-os k-rowspan-2"]/*/span/text()', isfirst=False)

        idx = pkind.get('idx')
        pname = phone.get('pname')
        klogger.info(f"result {idx}::{pname}")
        phone = json.dumps(phone)
        return phone

    def get_phones_info(self, phones: list):
        length = len(phones)
        for idx, pname in enumerate(phones):
            klogger.info(f"get phone [{idx:0>3d}::{length:0>3d}]{pname}")
            idxname = f"{idx}_{pname}"
            pkinds = gpi.get_phone_kinds(idxname=idxname, pname=pname)
            for pkind in pkinds:
                phone = gpi.get_phone_info(pkind)
                with open('./kimovil_phones.csv', 'a', encoding='utf-8') as f:
                    f.write(f'{phone}\n')

    def get_phones_pages(self, page: int):
        for page in range(1, page, 1):
            idxname = f'page_{page}'
            pkinds = gpi.get_phone_kinds(idxname=idxname, page=page)
            for pkind in pkinds:
                phone = gpi.get_phone_info(pkind)
                with open('./kimovil_page.csv', 'a', encoding='utf-8') as f:
                    f.write(f'{phone}\n')


if __name__ == '__main__':
    phones = ['CPH2083', 'CPH1937']
    gpi = GetPhoneInfo()
    gpi.get_phones_info(phones)
