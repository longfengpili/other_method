# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 11:22:47
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-23 11:33:54
# @github: https://github.com/longfengpili


import time
import random
import cloudscraper
from fake_useragent import UserAgent
from lxml.etree import Element as elem

from .base import PhoneBase

import logging
klogger = logging.getLogger(__name__)


class Kimovil(PhoneBase):
    KIND_PATH = '//div[@class="item-wrap"]'
    PKIND_SELECTOR = 'all'
    KIND_MPATHS = (
            ('mname', ('.//div[@class="title"]/text()', )),
            ('purl', ('.//a[@class="device-link"]/@href', )),
            ('prelease', ('.//div[@class="status available"]/text()', )),
        )

    def __init__(self):
        super(Kimovil, self).__init__(self.KIND_PATH, self.PKIND_SELECTOR, self.KIND_MPATHS)

    @property
    def base_url(self):
        base_url = 'https://www.kimovil.com/en/compare-smartphones'
        return base_url

    @property
    def scraper(self):
        scraper = cloudscraper.create_scraper()
        return scraper

    def base_request(self, url: str, try_times: int = 4):
        # print(url)
        status_code = 200

        scraper = self.scraper
        res = scraper.get(url)
        res_text = res.text
        noresult = 'Just a moment'
        while noresult in res_text and try_times > 0:
            klogger.warning(f'{url},  Error: {noresult} !')
            time.sleep(random.random() * 5)
            res = scraper.get(url)
            res_text = res.text
            try_times -= 1
            
        return res, status_code

    def request(self, pname: str = None, page: int = None):
        param = f'name.{pname}' if pname else f'page.{page}'
        url = f"{self.base_url}/{param}"
        res, status_code = self.base_request(url)
        return url, res
        
    def parse_phone(self, phone: elem):
        mpaths = (
            ('screen', ('.//li[@class="item item-screen k-rowspan-2"]//span/text()',)),
            ('size', ('.//li[@class="item item-size k-rowspan-2"]//span/text()',)),
            ('soc', ('.//li[@class="item item-soc k-rowspan-2"]//span/text()',)),
            ('antutu', ('.//li[@class="item item-antutu"]//span/text()',)),
            ('battery', ('.//li[@class="item item-battery"]//span/text()',)),
            ('os', ('.//li[@class="item item-os k-rowspan-2"]//span/text()',)),
        )

        phone_xpath = './/ul[@class="kiui-grid k-main k-auto-column device-mini-datasheet device-mini-datasheet-sheet"]'
        phone = self.get_elem(phone, phone_xpath)
        if phone:
            phone = phone[0]
            phone_info = self.get_elem_mpath(phone, *mpaths)
        else:
            phone_info = {'error': 'no response from server'}
        
        return phone_info
