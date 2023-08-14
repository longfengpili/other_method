# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 11:22:47
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 14:49:16
# @github: https://github.com/longfengpili

import cloudscraper
from lxml.etree import Element as elem

from .base import PhoneBase

import logging
glogger = logging.getLogger(__name__)


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

    def base_request(self, url: str):
        res = self.scraper.get(url)
        res = res.text
        return res

    def request(self, pname: str = None, page: int = None):
        param = f'name.{pname}' if pname else f'page.{page}'
        url = f"{self.base_url}/{param}"
        res = self.base_request(url)
        return res
        
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
        phone = self.get_elem(phone, phone_xpath)[0]
        phone_info = self.get_elem_mpath(phone, *mpaths)

        return phone_info
