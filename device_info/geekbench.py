# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-06-19 11:23:44
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-11 11:15:04

import time
import random
import json
import requests
from lxml import etree

import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
# LOGGING_CONFIG['handlers']['console']['formatter'] = 'color'
logging.config.dictConfig(LOGGING_CONFIG)
glogger = logging.getLogger(__name__)


class GetPhoneInfo:

    def __init__(self):
        self.url = 'https://browser.geekbench.com'
        self.is_v5cpu = False

    @property
    def headers(self):
        headers = {
            'Cookie': '_browse_session=B7U7kJoPc9ZGhUOnI87iXXoBGVOSFB7cdLqCePaN9nRrbrKurIKjJNM000s%2B3Hn%2F1X%2Fzuxeq%2Bnzheuiij0Ocb9E6rV2p7M5NWV51bnSq%2F1cq5cSrrQv0cU0ea6KtfxhGucqmplFHLWFWevZgqqhaJAWJ%2BasGb5QvSz%2Fm--rtR%2FHvz22%2BtTGsrA--SBxnSdo6e8EsST1U8Z0Aaw%3D%3D',  # noqa: E501
            'Host': 'browser.geekbench.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        return headers

    def requests_get(self, url: str, params: dict = None):
        headers = self.headers
        res = requests.get(url, headers=headers, params=params)
        res = res.text
        return res

    def get_page(self, pname: str, is_v5cpu: bool = False):
        url = f'{self.url}/search'
        params = {
            'utf8': '✓',
            'q': pname,
        }

        if is_v5cpu:
            self.is_v5cpu = True
            params['k'] = 'v5_cpu'
        else:
            self.is_v5cpu = False

        res = self.requests_get(url, params=params)
        return res

    def get_element_info(self, element: etree.Element, path: str, isfirst: bool = True):
        if element is None:
            return

        info = element.xpath(path)
        if not info:
            info = None
        elif isfirst:
            info = info[0]
        else:
            info = '||'.join([i.strip() for i in info])

        if isinstance(info, str):
            info = info.strip()
            info = info.replace('\n', ' ')
        return info

    def get_element_tr(self, tr: etree.Element):
        name = self.get_element_info(tr, './/td[1]/text()')
        value = self.get_element_info(tr, './/td[2]/text()')

        if not value:
            value1 = self.get_element_info(tr, './/td[2]/a/text()')
            value2 = self.get_element_info(tr, './/td[2]/a/@href')
            value2 = self.url + value2
            value = [value1, value2]

        return name, value

    def get_element_trs(self, trs: list):
        elems = {}
        for tr in trs:
            _name, _value = self.get_element_tr(tr)
            elems[_name] = _value
        return elems

    def get_page_by_rightapi(self, pname: str):
        res = self.get_page(pname)
        nomatch = 'not match any Geekbench 6 CPU'
        if nomatch in res:
            glogger.warning(f'{pname} {nomatch} !')
            res = self.get_page(pname, is_v5cpu=True)

        return res

    def get_pkind_info(self, idx: str, pname: str):
        def parse_phone(pkind):
            pinfo = {}
            pinfo['idx'] = f"{idx}_{pname}"
            pinfo['idx_name'] = pname
            pinfo['pname'] = self.get_element_info(pkind, './/div[@class="col-12 col-lg-4"]/a/text()')
            purl = self.get_element_info(pkind, './/div[@class="col-12 col-lg-4"]/a/@href')
            pinfo['purl'] = self.url + purl if purl else self.url
            pinfo['psoc'] = self.get_element_info(pkind, './/div[@class="col-12 col-lg-4"]/span[2]/text()')
            pinfo['sc_score'] = self.get_element_info(pkind, './/div[@class="col-6 col-md-3 col-lg-2"][3]/span[2]/text()')
            pinfo['mc_score'] = self.get_element_info(pkind, './/div[@class="col-6 col-md-3 col-lg-2"][4]/span[2]/text()')
            return pinfo

        res = self.get_page_by_rightapi(pname)
        html = etree.HTML(res)

        # main page
        pkind = self.get_element_info(html, './/div[@class="col-12 list-col"]')
        pkind = parse_phone(pkind)
        return pkind

    def parse_phone_v5(self, html: etree.Element):
        phone = {}

        # System Information
        system_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][1]/tbody/tr'
        system_trs = html.xpath(system_path)
        system_elems = self.get_element_trs(system_trs)
        phone.update(system_elems)

        # CPU Information
        cpu_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][2]/tbody/tr'
        cpu_trs = html.xpath(cpu_path)
        cpu_elems = self.get_element_trs(cpu_trs)
        phone.update(cpu_elems)

        # Memory Information
        memory_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][3]/tbody/tr'
        memory_trs = html.xpath(memory_path)
        memory_elems = self.get_element_trs(memory_trs)
        phone.update(memory_elems)

        return phone

    def parse_phone_v6(self, html: etree.Element):
        phone = {}
        # System Information
        system_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"]/tbody/tr'
        system_trs = html.xpath(system_path)
        system_elems = self.get_element_trs(system_trs)
        phone.update(system_elems)

        # CPU Information
        cpu_path = './/div[@class="table-wrapper"][3]/table[@class="table system-table"]/tbody/tr'
        cpu_trs = html.xpath(cpu_path)
        cpu_elems = self.get_element_trs(cpu_trs)
        phone.update(cpu_elems)

        # Memory Information
        memory_path = './/div[@class="table-wrapper"][4]/table[@class="table system-table"]/tbody/tr'
        memory_trs = html.xpath(memory_path)
        memory_elems = self.get_element_trs(memory_trs)
        phone.update(memory_elems)

        return phone

    def get_device_info(self, url: str):
        device_info = {}
        res = self.requests_get(url)
        html = etree.HTML(res)

        # Device Information
        device_path = './/div[@class="table-wrapper"][1]/table[@class="table system-table"]/tbody/tr'
        device_trs = html.xpath(device_path)
        device_elems = self.get_element_trs(device_trs[1:])
        device_info.update(device_elems)
        return device_info

    def get_phone_info(self, pkind: dict):
        phone = {}
        phone.update(pkind)
        time.sleep(random.random() * 5)
        purl = pkind.get('purl')
        res = self.requests_get(purl)
        html = etree.HTML(res)

        if self.is_v5cpu:
            _phone = self.parse_phone_v5(html)
        else:
            _phone = self.parse_phone_v6(html)
        phone.update(_phone)

        model = _phone.get('Model')
        if isinstance(model, list):
            device_info = self.get_device_info(model[1])
            phone.update(device_info)

        idx = pkind.get('idx')
        pname = phone.get('pname')
        glogger.info(f"result {idx}::{pname}")
        phone = json.dumps(phone)
        return phone

    def get_phones_info(self, phones: list, idx_from: int = 0):
        length = len(phones)
        for idx, pname in enumerate(phones):
            idx += idx_from
            glogger.info(f"get phone [{idx:0>3d}::{length:0>3d}]{pname}")
            pkind = self.get_pkind_info(idx=idx, pname=pname)
            phone = self.get_phone_info(pkind)
            with open('./geekbench_phones.csv', 'a', encoding='utf-8') as f:
                f.write(f'{phone}\n')


if __name__ == '__main__':
    phones = ['samsung SM-A025F', '2206122SC']  # 
    gpi = GetPhoneInfo()
    gpi.get_phones_info(phones)
