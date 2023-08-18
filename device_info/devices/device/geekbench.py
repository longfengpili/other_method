# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 15:27:12
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-18 12:08:51
# @github: https://github.com/longfengpili

from lxml.etree import Element as elem

from .base import PhoneBase

import logging
glogger = logging.getLogger(__name__)


class Geekbench(PhoneBase):
    KIND_PATH = './/div[@class="col-12 list-col"]'
    PKIND_SELECTOR = 'first'
    KIND_MPATHS = (
            ('mname', ('.//div[@class="col-12 col-lg-4"]/a/text()', )),
            ('purl', ('.//div[@class="col-12 col-lg-4"]/a/@href', )),
            ('psoc', ('.//div[@class="col-12 col-lg-4"]/span[2]/text()', )),
            ('sc_score', ('.//div[@class="col-6 col-md-3 col-lg-2"][3]/span[2]/text()', )),
            ('mc_score', ('.//div[@class="col-6 col-md-3 col-lg-2"][4]/span[2]/text()', ))
        )

    def __init__(self):
        self.is_v5cpu = False
        super(Geekbench, self).__init__(self.KIND_PATH, self.PKIND_SELECTOR, self.KIND_MPATHS)

    @property
    def base_url(self):
        base_url = 'https://browser.geekbench.com'
        return base_url

    # @property
    # def headers(self):
    #     headers = {
    #         'Host': 'browser.geekbench.com',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    #     }
    #     return headers

    def request(self, pname: str):
        url = f"{self.base_url}/search"
        params = {
            'utf8': '✓',
            'q': pname
        }

        self.is_v5cpu = False
        res, status_code = self.base_request(url, params)
        res_text = res.text if status_code == 200 else ''
        nomatch = 'not match any Geekbench 6 CPU'
        if nomatch in res_text:
            glogger.warning(f'{pname} {nomatch} !')
            params['k'] = 'v5_cpu'
            self.is_v5cpu = True
            res, status_code = self.base_request(url, params)

        return url, res
        
    def parse_phone(self, phone: elem):
        phone_info = {}
        is_v5cpu = self.is_v5cpu
        kpaths = ('.//td[1]/text()', )
        vpaths = ('.//td[2]/text()', './/td[2]/a/text()', './/td[2]/a/@href')
        # print(is_v5cpu)

        if is_v5cpu:
            system_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][1]/tbody/tr'
            cpu_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][2]/tbody/tr'
            memory_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"][3]/tbody/tr'
        else:
            system_path = './/div[@class="table-wrapper"][2]/table[@class="table system-table"]/tbody/tr'
            cpu_path = './/div[@class="table-wrapper"][3]/table[@class="table system-table"]/tbody/tr'
            memory_path = './/div[@class="table-wrapper"][4]/table[@class="table system-table"]/tbody/tr'

        # System Information
        system = self.get_elem(phone, system_path)
        system_elems = self.get_elems_kv(system, kpaths, vpaths)
        phone_info.update(system_elems)

        # CPU Information
        cpu = self.get_elem(phone, cpu_path)
        cpu_elems = self.get_elems_kv(cpu, kpaths, vpaths)
        phone_info.update(cpu_elems)

        # Memory Information
        memory = self.get_elem(phone, memory_path)
        memory_elems = self.get_elems_kv(memory, kpaths, vpaths)
        phone_info.update(memory_elems)

        return phone_info
